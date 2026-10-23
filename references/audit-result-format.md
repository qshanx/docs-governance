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

## 路径与扫描边界

Markdown 本地链接是明确引用，目标缺失仍为 `links.local / fail`；兼容 `文件:行号` 和 `文件:行号:列号`，检查文件存在，不验证行列范围。`spine` 单独执行时也检查入口／载体中的链接；`full` 在 artifacts 中统一检查，避免重复计数。配置 `required_files` 仍是必需文件的确定性约束。

反引号中的路径可能是禁止项、路由、例子或阅读提示，不能仅凭不存在判定失败。`spine.paths` 对缺失候选按源文件汇总为 `warning`，`evidence.candidates` 保留每处 `target` 和一基 `line`，由 Agent 按上下文判断；代码块和显式可选项不列候选。需要机械强制存在的入口应使用 Markdown 链接或项目配置，不以“必读”字样猜自然语言。JSON 字段、状态含义及退出码不变。

Git 项目的 artifacts 和 ADR 枚举采用已跟踪文件及未被 Git 忽略的未跟踪文件；已跟踪文件即使匹配忽略规则仍检查。原固定排除 `.git`、`.governance`、`.venv`、`node_modules`、`__pycache__`、`vendor` 保留。非 Git 项目只按该固定列表遍历，不读取项目外目录。忽略目录不等于已验证；显式链接的目标与配置必需项仍独立检查。未被忽略的历史副本仍可能报告断链，不能据此自动改写历史或宣告当前业务失败。

## TEST-ID 识别边界

`tests.references` 只识别独立、完整的 TEST-ID，引用与 `TESTS.md` 登记共用同一边界，大小写不敏感。`XY-TEST-CENTER-UX-20260922` 等带连字符前缀或后缀的文档编号不被截取为测试编号，也不能冒充台账登记。

同一文档中的真实测试引用仍逐项核对：台账存在但未登记时返回 `fail`／退出 1；未启用台账时仍报告 `unverified`。已有模板目录排除和显式示例标记规则不变，不因出现文档编号跳过整份材料；JSON 字段与退出码约定不变。

## ADR 范围兼容轻量记录

`adr` 范围检查根目录及上下文中的 `docs/adr/`，排除已有忽略目录。README 索引和状态均可选：缺省以 `adr.index`／`adr.status` 的 `unverified` 说明覆盖边界，不因此失败，也不推定决策已批准。显式状态仍校验 proposed／accepted／deprecated／superseded，兼容 `superseded by ADR-NNNN` 并在该 ADR 目录核对目标。已有索引漏登或断链、ADR 本地断链、非法或空状态及不存在的替代目标仍退出 1。

原先“索引或状态缺少即失败”的默认政策由阿磊于 2026-10-12 授权调整，以兼容 Matt 的轻量 ADR；`schema_version` 仍为 1，字段与状态含义不变，仅调整这些检查条件。它不是通用 Markdown／YAML 解析器，也不执行项目自定义的审批政策；导航、理由、批准证据与模块内联决策仍需语义核对。
