# 文档治理审查修复与验证

日期：2026-09-05。范围：评审写回保护、确定性审计、共享流程、机器契约模板及本插件自治理文档。

## 修复证据

| 问题 | 修复 | 回归证据 |
|---|---|---|
| 评审期间新正文被旧快照覆盖，已删除文件被重建 | 写回前核对完整文件内容；变化时失败且不保存通过状态 | TEST-REVIEW-001：编辑、删除和重新评审 |
| 删除区上层标题导致漏报，替代物被误认作删除目标 | 匹配实际章节与表格路径列 | TEST-AUDIT-001：真实 STATUS 模板与替代物正反例 |
| 已提交的历史改写逃过 HEAD 检查 | 显式基线、缺失基准失败、整份 LOG 删除仍核对归档 | TEST-AUDIT-001：两次真实 Git 提交 |
| 引用式断链漏检，day-0 可选桥接误报 | 检查引用定义；可选路径按行显式声明 | TEST-AUDIT-001：引用链接、代码示例和 AGENTS 模板 |
| 依赖相邻仓库，本机全绿无法移植 | 外部材料改为来源说明，不保留不可移植活动链接 | TEST-AUDIT-001：独立目录复制后 full 审计 |
| 无标题前缀的日志被计为零事件 | 统一标准事件格式，解析错误时失败且保留原文 | TEST-LOG-001：201 条错误格式事件 |
| commands/agents 与 Skill 重复规则 | 共享模式和角色规则归 Skill，适配层只传参及选择角色 | Skill 格式校验、人工检查依赖方向和读写边界 |
| 契约示例不能直接驱动机器验证 | OpenAPI 是唯一字段来源，CONTRACT 只登记入口 | TEST-CONTRACT-TEMPLATE-001：标准校验及 JSON 序列化正反例 |

修复前新增回归测试复现了 8 个失败场景；修复后默认 runner 共 28 个测试通过。标准验证命令（激活项目虚拟环境后）：

```bash
DOCS_GOVERNANCE_BASE_REF=origin/main bash scripts/verify.sh
```

验证包含双端 manifest、路由、引用、Python 编译、测试、机器契约和 full 文档审计。依赖安装需要网络；测试本身不调用实际模型或线上业务服务。PR CI 使用目标分支基线，push CI 使用推送前 SHA。

2026-09-05，[PR #3](https://github.com/qshanx/docs-governance/pull/3) 的修复提交 `c132f0a` 已通过 Ubuntu / Python 3.12 的 [push 检查](https://github.com/qshanx/docs-governance/actions/runs/33958218000)和 [pull_request 检查](https://github.com/qshanx/docs-governance/actions/runs/33958226055)。此记录只证明该提交；后续提交与合并结果以对应 GitHub checks 为准。

## 空项目初始化复跑

当前 Codex 按新的 Skill“空项目初始化”模式在临时 Git 仓执行：

- 生成 AGENTS、CLAUDE、PROJECT_LOG、docs/governance 四份文件。
- CLAUDE 12 行；未预建可选治理文件。
- git init 后安装可执行 pre-commit；full 文档审计通过。
- 首提 `5b21cf910d16a40e944f13dde2f9a85c072df7d1`，提交后工作区干净。

此证据验证共享流程，不代表 Claude Code 原生 slash command 已通过宿主验收。

## 边界

- 保留既有业务项目试点、Claude Code 原生命令和 Stop hook 行为测试缺口；未把它们宣称为本次完成。
- OpenAPI 模板测试只证明模板和响应约束，不证明用户项目已完成消费方生成、服务实现或真实联调。
- 可选标记仅豁免声明路径尚不存在；已存在文档内容继续检查。TEST-ID 字符串检索和孤儿提示仍需语义层复核。
- 源码版本保持 0.7.0，本轮进入 Unreleased；合并代码不等于发布新版本或更新宿主已缓存的插件。
