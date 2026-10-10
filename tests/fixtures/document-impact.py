"""Create an isolated Git fixture for an Agent's document-impact review."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def create_fixture(root, case):
    # Never replace an existing directory or change the caller's Git repository.
    root.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for key in tuple(env):
        if key.startswith('GIT_'):
            env.pop(key)

    def run(*args):
        return subprocess.run(args, cwd=root, env=env, text=True, capture_output=True,
                              check=True, timeout=30).stdout.strip()

    def put(name, text):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def put_json(name, value):
        put(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

    def commit(message):
        run('git', 'add', '.')
        run('git', 'commit', '-qm', message)
        return run('git', 'rev-parse', 'HEAD')

    def interface(field, internal=False):
        put_json('schema/order.json', {
            'type': 'object', 'properties': {field: {'type': 'integer', 'minimum': 0}},
            'required': [field], 'additionalProperties': False,
        })
        expression = f'dict({field}=100)' if internal else repr({field: 100})
        put('src/api.py', 'import json\n\ndef get_order():\n'
            f'    return json.loads(json.dumps({expression}))\n\n'
            'def get_inventory():\n    return {"total": 3}\n')
        receipt = run(sys.executable, '-c',
                      'import json; from src.api import get_order; print(json.dumps(get_order()))')
        put_json('evidence/response.json', {
            'response': json.loads(receipt),
            'source_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                              for name in ('src/api.py', 'schema/order.json')},
        })

    run('git', 'init', '-q', '-b', 'main', '--template=')
    for key, value in (('user.name', 'Document Impact Fixture'),
                       ('user.email', 'fixture@example.invalid'),
                       ('commit.gpgsign', 'false'),
                       ('core.hooksPath', str(root / '.git/disabled-hooks'))):
        run('git', 'config', key, value)
    put_json('.docs-governance.json', {
        'version': 1, 'required_files': ['README.md'],
        'change_rules': [{'id': 'order-api', 'include': ['src/*', 'schema/order.json'],
                          'documents': ['CONTRACT.md', 'TESTS.md', 'docs/api.md', 'docs/consumer.md']}],
    })
    guides = ['api', 'consumer', 'integration', 'reference', 'history', 'inventory', 'decision', 'faq']
    put('README.md', '# Order sample\n\n[契约](CONTRACT.md) · [证据](TESTS.md)\n\n' +
        '\n'.join(f'- [{name}](docs/{name}.md)' for name in guides) + '\n')
    put('CLAUDE.md', '# 样例规则\n\n订单字段以 [契约](CONTRACT.md) 为准；'
        '已有说明沿 [入口](README.md) 查找。\n')
    put('CONTRACT.md', '# 订单接口\n\n唯一机器定义：[订单响应](schema/order.json)。\n'
        '命名依据：[当前决定](docs/decision.md)。版本以所在 Git 提交为准。\n')
    put('TESTS.md', '# 验证入口\n\n[序列化输出与输入哈希](evidence/response.json)'
        '是自动生成的运行回执，不代表业务验收结论。\n')
    for name in ('api', 'consumer', 'integration'):
        put(f'docs/{name}.md', f'# {name}\n\n订单金额读取 `get_order()["total"]`。\n'
            '字段定义见 [订单契约](../schema/order.json)。\n')
    # Keep the inline example on line 3 for existing impact-location tests.
    with (root / 'docs/api.md').open('a') as file:
        file.write("\n在样例根目录，使用 Python 3 标准库运行；预期输出 100（分）：\n\n"
                   "```bash\n"
                   "python3 -c 'from src.api import get_order; print(get_order()[\"total\"])'\n"
                   "```\n")
    put('docs/reference.md', '# 接口导航\n\n字段直接读取 [机器契约](../schema/order.json)。\n')
    put('docs/history.md', '# 历史记录\n\n历史 v1 曾用 `get_order()["total"]` 读取金额。\n'
        '当前版本请从 [契约入口](../CONTRACT.md) 读取，本页不是当前调用指南。\n')
    put_json('schema/inventory.json', {'type': 'object', 'properties': {'total': {'type': 'integer'}}})
    put('docs/inventory.md', '# 库存接口\n\n库存数量读取 `get_inventory()["total"]`。\n'
        '依据 [库存契约](../schema/inventory.json)，与订单金额无关。\n')
    decision = '订单 API 金额字段采用 `total`，单位为分。\n'
    put('docs/decision.md', '# 当前命名决定\n\n' + decision)
    put('docs/faq.md', '# FAQ\n\n命名以 [当前决定](decision.md) 为准。\n')
    put('PROJECT_LOG.md', '## [2026-10-09] init | 创建合成样例\n')
    interface('total')
    base = commit('Create document impact baseline')
    if case == 'interface':
        interface('total_amount')
        decision = decision.replace('`total`', '`total_amount`')
        put('docs/decision.md', '# 当前命名决定\n\n' + decision)
        put('docs/faq.md', '# FAQ\n\n' + decision)
        with (root / 'docs/consumer.md').open('a') as file:
            file.write('\n补充：本轮实现已调整。\n')
        event = '样例确认 total → total_amount，以明确金额含义；[依据](docs/decision.md)'
    else:
        interface('total', internal=True)
        event = '调整字典构造方式，对外响应不变'
    with (root / 'PROJECT_LOG.md').open('a') as file:
        file.write(f'\n## [2026-10-09] change | {event}；[回执](evidence/response.json)\n')
    head = commit('Apply document impact scenario')
    return {'root': str(root), 'base': base, 'head': head, 'case': case}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='New directory; existing paths are refused')
    parser.add_argument('--case', choices=('interface', 'internal'), default='interface')
    args = parser.parse_args()
    print(json.dumps(create_fixture(args.directory.resolve(), args.case), ensure_ascii=False))
