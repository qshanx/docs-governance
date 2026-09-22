"""项目声明的文件位置规则；不执行配置中的任何命令。"""
from fnmatch import fnmatchcase
import json
import os
from pathlib import Path

POLICY_NAME = '.docs-governance.json'
IGNORED = {'.git', '.governance', '.venv', 'node_modules', '__pycache__', 'vendor'}


def files_under(root):
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED and not Path(directory, d).is_symlink())
        for name in sorted(files):
            yield Path(directory, name)


def string_list(value, name, nonempty=False):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f'{name} 必须是非空字符串的数组')
    if nonempty and not value:
        raise ValueError(f'{name} 不能为空')
    return value


def relative_name(value):
    return isinstance(value, str) and value and not value.startswith('/') and '..' not in value.split('/') and '\\' not in value


def read_policy(root):
    path = root / POLICY_NAME
    if path.is_symlink():
        raise ValueError('规则文件不能是软链接')
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1:
        raise ValueError('规则 version 必须为 1')
    if set(data) - {'version', 'required_files', 'placement', 'auto_audit'}:
        raise ValueError('规则包含未知字段')
    required = string_list(data.get('required_files', []), 'required_files')
    if any(not relative_name(p) or any(c in p for c in '*?[') for p in required):
        raise ValueError('required_files 必须是仓库内的具体相对路径')
    rules = data.get('placement', [])
    if not isinstance(rules, list):
        raise ValueError('placement 必须是数组')
    ids = set()
    for rule in rules:
        if not isinstance(rule, dict) or set(rule) - {'id', 'include', 'exclude', 'heading_keywords', 'allowed_dirs'}:
            raise ValueError('位置规则包含未知字段或格式错误')
        name = rule.get('id')
        if not isinstance(name, str) or not name or name in ids:
            raise ValueError('位置规则 id 必须非空且唯一')
        ids.add(name)
        for key in ('include', 'allowed_dirs'):
            string_list(rule.get(key), key, nonempty=True)
        for key in ('exclude', 'heading_keywords'):
            string_list(rule.get(key, []), key)
        if any(not relative_name(p) for key in ('include', 'exclude', 'allowed_dirs') for p in rule.get(key, [])):
            raise ValueError('规则路径不得越出仓库')
        if any(any(c in p for c in '*?[') for p in rule['allowed_dirs']):
            raise ValueError('allowed_dirs 必须是具体目录，不能使用通配符')
    auto = data.get('auto_audit', {})
    if not isinstance(auto, dict) or set(auto) - {'on_stop'}:
        raise ValueError('auto_audit 格式错误')
    if 'on_stop' in auto and not isinstance(auto['on_stop'], bool):
        raise ValueError('on_stop 必须是布尔值')
    return data


def main_heading(text):
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(('```', '~~~')):
            marker = stripped[:3]
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence is None and line.startswith('# '):
            return line[2:].strip().casefold()
    return ''


def check_policy(root, report):
    try:
        policy = read_policy(root)
        if policy is None:
            return
        for relative in policy.get('required_files', []):
            path = root / relative
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                report.add('policy.required', 'fail', f'必需文件缺失或不是仓库内普通文件：{relative}', path=relative)
        for path in files_under(root):
            relative = path.relative_to(root).as_posix()
            for rule in policy.get('placement', []):
                if not any(fnmatchcase(relative, p) for p in rule['include']):
                    continue
                if any(fnmatchcase(relative, p) for p in rule.get('exclude', [])):
                    continue
                if path.is_symlink():
                    report.add('policy.placement', 'fail', f'受约束文件不能通过软链接绕过位置检查：{relative}', path=relative)
                    continue
                keywords = rule.get('heading_keywords', [])
                if keywords and not any(k.casefold() in main_heading(path.read_text(encoding='utf-8')) for k in keywords):
                    continue
                if not any(relative.startswith(d.rstrip('/') + '/') for d in rule['allowed_dirs']):
                    report.add('policy.placement', 'fail', f'{relative} 命中 {rule["id"]}，应放在 {", ".join(rule["allowed_dirs"])}',
                               path=relative, evidence={'rule': rule['id'], 'allowed_dirs': rule['allowed_dirs']})
        if not any(f.check.startswith('policy.') and f.status in ('fail', 'error') for f in report.findings):
            report.add('policy.placement', 'pass', '项目必需文件与内容位置规则通过')
    except (ValueError, OSError, UnicodeError) as exc:
        report.add('policy.config', 'error', f'文档位置规则检查未完成：{exc}', path=POLICY_NAME)
