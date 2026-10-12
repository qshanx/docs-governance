# 文档审计结果接口

`scripts/audit-docs.py` 的同一组检查生成结果，再渲染为终端文字或 JSON；默认仍为文字。JSON 供 CI、Agent 或其他工具读取，不需要解析中文提示。

## 调用

从目标项目目录调用插件中的 Shell 入口，也可显式指定项目：

```bash
python3 scripts/audit-docs.py --root /path/to/project --scope full --base-ref main --format json
bash scripts/audit-cheap.sh full --format json
```

Shell 入口沿用 `DOCS_GOVERNANCE_ROOT` 和 `DOCS_GOVERNANCE_BASE_REF`。JSON 模式在 stdout 输出单个对象；正确解析参数后的文档失败、无效目录、无效基线和读取错误都使用该格式。参数拼写或取值错误由 argparse 输出到 stderr，退出码为 2。

## 结果与退出码

| status | 含义 | 退出码 |
|---|---|---|
| `pass` | 本次执行的确定性检查没有发现失败、警告或未验证项 | 0 |
| `warning` | 有启发式提示或维护建议，需人工判断 | 0 |
| `unverified` | 缺少基准或可选载体等，部分结论无法验证 | 0 |
| `fail` | 已发现可机械证明的文档问题，如断链或历史改写 | 1 |
| `error` | 参数所指对象无效、文件不可读或 Git 操作失败等，检查未完成 | 2 |

汇总优先级为 `error > fail > unverified > warning > pass`。可选载体缺失不会强迫项目补齐文档，但仍以 `unverified` 告知覆盖边界。退出码 0 只表示没有确定性失败或执行错误，不代表业务验收或语义审计通过。

## 字段约定

`schema_version` 当前为 1。新增可选字段可向后兼容；改变既有字段含义或状态取值时应升级版本，消费者遇到不支持的版本须报告无法解释，不能默认通过。

| 字段 | 用途 |
|---|---|
| `root`、`scope` | 本次目标项目绝对路径及请求的审计范围 |
| `generated_at` | 结果生成时间，UTC ISO 8601 |
| `requested_base_ref`、`base_ref` | 请求的日志比较基线及解析后的 commit；未指定、无法解析或范围不涉及日志时可为 null |
| `head_commit`、`worktree_dirty` | 执行时观测到的 HEAD 和工作区是否有改动；无 Git 仓或无提交时不可用字段为 null |
| `status`、`exit_code`、`counts` | 汇总结论、进程退出码和各结果类型的数量；数量按结果记录计算，不代表测试覆盖率 |
| `findings` | 逐条结果：`check` 稳定检查标识、`status`、所属 `scope`、人读 `message`、`path`、`line` 和机器可读 `evidence` |

`path` 通常相对于 root；无效根目录可为绝对路径，集合检查可为 null。`line` 为已知时的一基行号，否则为 null。`evidence` 按检查提供目标路径、缺失编号、计数或异常类型等；不适用时为空对象。不要通过解析 `message` 判断结果。

未执行的检查不产生记录；`findings` 只描述所选范围及实际执行的检查。Git 基线只用于日志历史比较，其他检查读取当前工作区。输出没有冻结文件系统，也没有缓存评审通过状态；`head_commit` 不能唯一标识未提交内容，后续相关变更发生后应重新运行。保存结果时还应遵循项目已有的证据与访问约定。

结构化输出通过 `tests/test_audit_docs.py` 的真实 CLI / Shell 调用验证；共享日志格式在 `scripts/logformat.py` 维护，归档后历史一致性由 `tests/test_project_log_index.py` 验证。

## ADR 范围兼容轻量记录

`adr` 范围检查根目录及上下文中的 `docs/adr/`，排除已有忽略目录。README 索引和状态均可选：缺省以 `adr.index`／`adr.status` 的 `unverified` 说明覆盖边界，不因此失败，也不推定决策已批准。显式状态仍校验 proposed／accepted／deprecated／superseded，兼容 `superseded by ADR-NNNN` 并在该 ADR 目录核对目标。已有索引漏登或断链、ADR 本地断链、非法或空状态及不存在的替代目标仍退出 1。

原先“索引或状态缺少即失败”的默认政策由阿磊于 2026-10-12 授权调整，以兼容 Matt 的轻量 ADR；`schema_version` 仍为 1，字段与状态含义不变，仅调整这些检查条件。它不是通用 Markdown／YAML 解析器，也不执行项目自定义的审批政策；导航、理由、批准证据与模块内联决策仍需语义核对。
