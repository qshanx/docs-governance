# 测试上线

## DM-20261012：直接复用领域建模

来源为本会话的复用与实测授权。固定引入 Matt `c55ee46073ed923f86ce59a5eb3b6d895095d1b7` 的 domain-modeling；三份方法／格式原文件的 Git blob 已与上游核对，SKILL 仅追加项目适配指针。旧入口与模板保留兼容路标，重复的术语澄清、八字段 ADR 流程不再维护。

先补 ADR 回归再改审计：旧实现出现 4 项失败，分别涉及轻量记录、编号替代状态、上下文子目录漏查及无索引时跳过断链；修改后 ADR 专项 9 项与整个审计组 38 项通过。缺索引／状态改为未验证且不阻断，显式非法状态、已有索引漏登、断链及不存在的替代目标仍拒绝；不将无状态推定为批准。

实际调用使用两个隔离 Codex CLI 会话，读取当前工作区 Skill，不接触业务源项目；证据保留在 `/private/tmp/domain-modeling-real-ZZouBL/`：

- 建档正例：不点名 Skill，要求为已有库存模块补文档；实际读取 module-governance、domain-modeling 及适配。新增模块 AGENTS 与 CONTEXT，更新已有 CONTEXT-MAP；只沉淀负责人确认的两个库存术语，没有把 Ordering／Billing 含义不同的 Account 强行统一，也没有新造 GLOSSARY、ADR 索引或 LOG。已有 ADR、源码、测试前后 SHA-256 相同。
- 行为与语义核对：2 项库存测试通过；full、artifacts、adr 审计均退出 0；项目／模块入口分别 9／24 行，长度检查通过。独立重跑测试与 artifacts／adr 结果一致，生成链接可达。产物明确指出公开 available 尚可被直接写入、PostgreSQL 尚未实现、真实消费方集成缺证据；没有把开发约束当成运行时隔离。无状态 ADR 保留未验证提示，不声称已批准；缺索引的导航另行人工核对。
- 兼容与只读负例：通过 context-and-decisions 仅讨论“Customer／User 都叫账号”和未来拆模块；实际读取兼容入口、Matt 方法与适配，指出购买主体和登录身份不同及模块不等于业务上下文，提出澄清而未落盘。前后仍只有原 AGENTS、CONTEXT 两份项目文件，SHA-256 相同，增改删为 0。
- 仓库验证：既有 `.venv` 内运行 `bash scripts/verify.sh` 退出 0，当前混合工作区全部 124 项测试通过，包含本轮审计回归；结构／路由、双端 manifest、插件引用及 full 文档审计通过。新主入口和兼容入口的 quick_validate 均有效，`git diff --check` 通过。两份 FORMAT 的 Git blob 与固定上游完全一致。

宿主启动有既存本地 MCP 连接警告，未影响上述会话完成；没有验证 Claude Code 原生加载、跨会话触发、真实业务接入或完整 DDD 实现。两份入口是协作文档载体，不是完整领域设计。本轮不提交、推送、安装到业务项目或发布；124 项仅是当前工作区结果，不作为远端 CI 或本轮独有测试数量。

后续提交授权与隔离验证（2026-10-12）：阿磊明确要求提交推送、创建 PR，检查和评审无问题后合并 main；此前“不提交／推送”描述的是实施阶段。以远端 main `4ee5a00` 建立干净分支，仅提取 DM-20261012，不携带其他协作体系、环境或历史修复。适配中的历史主源指针链接既有记录约定正文，不依赖未提交的新章节。激活原项目已有 `.venv` 在隔离仓库运行完整 verify：119 项测试、插件结构、路由与 full 文档审计通过，退出 0；另有 5 项无关引用检查测试只在原混合工作区，不进入此 PR。提交快照、CI 与独立评审以 PR 最新 head 回执为准。

适用主题：产品需求与迭代治理 r1。记录日期：2026-09-22。阶段状态：已完成（本轮本地文档验证）；发布不在本轮范围。

## 输入与环境

验收依据：[PRD r1](06-prd.md)。实现版本以 [草稿 PR #12](https://github.com/qshanx/docs-governance/pull/12) 的提交为准；以下记录为本轮本地验证，尚未发布。环境为本仓库 `.venv`，未访问生产服务，未进行业务项目端到端试点。

## 实际验证结果

| 检查 | 实际结果 |
|---|---|
| 激活 `.venv` 后运行 `bash scripts/verify.sh` | 退出码 0；双端 manifest、9 个 Skill 的路由和说明、路径引用、Python 编译与 full 文档审计通过 |
| 标准入口中的 Python 单元测试 | 72 个通过；验证的是现有确定性工具，不代表新 Skill 的业务效果已验证 |
| 使用 skill-creator 的 `quick_validate.py` 检查新 Skill | 退出码 0，输出 Skill is valid |
| `git diff --check` | 退出码 0，无空白错误 |
| PE-1 至 PE-4 文本审查 | 见 [需求评审](07-requirements-review.md) |

full 审计提示本项目未建立 CONTEXT；现有规则允许按需创建，无稳定词汇问题时不补空壳。本轮新增规则校验、Stop 内容指纹缓存、暂存快照检查及其 13 个行为测试。

PR 前护栏追加 10 个集成测试：真实本地 bare remote 上断链推送被阻断、修复后及再次推送成功；未提交修复不能覆盖已提交断链；子目录、linked worktree、显式来源 SHA、重命名／删除、排除项、关联文档缺失、错误基线、错误配置及日志历史改写均按预期处理。源仓库 index 与 HEAD 保持不变。宿主原生 Stop、其他业务项目安装、远端分支保护仍不在本轮验证范围。

## 发布与后续

2026-09-23 PR 评审修复验证：原钩子在 `src/` 调用对错放 PRD 不输出任何提示，新增回归先失败；修复后从根、`src/` 和更深目录产生相同违规报告，并共享根缓存。追加 8 个场景覆盖独立子配置（含禁用）、显式根覆盖与无效根、嵌套仓库隔离、非 Git／旧四件套、直接 CLI、损坏／目录／软链接配置和 linked worktree。位置／Stop 测试合计 21 个通过，全套 72 个及 verify 通过；仍是原始 Bash 钩子测试，未验证 Claude Code 原生事件派发。

2026-09-23 r2 管理员角色验证：标准 verify 与 64 项现有测试通过，两个修改过的 Skill 均通过格式验证，新增 Agent 的元数据按现有适配层格式解析通过，`git diff --check` 通过。PE-8 的五个文本场景见需求评审记录。本轮只增加角色、规范和模板，不新增镜像文本断言测试；未运行 Claude Code 原生角色调度，不据此宣称业务试点完成。

发布状态：未发布。上线状态：未上线。提交已推送并创建草稿 PR，未执行部署。每次新提交仍以 PR 最新 checks 为准，不沿用旧提交的绿色结论。若后续发布，应使用对应提交重新验证并记录版本；运营结果进入 [运营反馈](10-operations-feedback.md)。

2026-09-23 r3 按任务读取验证：完整 verify、现有 72 项测试、product-evolution 的 Skill 格式验证及 diff 空白检查通过。PE-9／PE-10 的七个文本场景见需求评审；未新增镜像规范的断言测试，未做独立 Agent 读取轨迹或上下文压力测试。本轮未修改执行脚本，已有审计仍只证明结构与引用检查结果。

2026-09-27 r4 已有项目首次接入验证：在仓库 `.venv` 中运行 `bash scripts/verify.sh`，退出码 0；新增 command 委托共享 Skill 检查通过，Python 编译、72 项单元测试、full 文档审计及既有结构检查均通过，`git diff --check` 通过。PE-11／PE-12 的探测、草案、确认、最小写入和三入口分工场景见需求评审。Claude Code 未在本轮真实加载 `/governance-setup`，因此宿主端到端交互与业务项目首次接入仍未验证。

2026-09-27 r5 入口规范验证：本地 `bash scripts/verify.sh` 返回 0，10 个 Skill 路由与用户说明、72 项现有单元测试、链接及位置审计通过。agent-entrypoints、living-docs-governance、product-evolution 均通过 quick_validate，`git diff --check` 通过。ENP-1 至 ENP-4 的六个规范场景见需求评审；未新增镜像文字的断言测试，未运行独立宿主会话或业务项目生成试点。本轮没有推送、合并或发布；这些结果不代替统一 setup 的验收。

2026-09-27 r5 八条规范及 ENP-5 补充验证：重跑 `bash scripts/verify.sh` 返回 0，72 项现有测试通过；本次修改的 agent-entrypoints 和 living-docs-governance 通过 quick_validate，diff 空白检查通过。原文 1—8 与规范的对应关系及边界见 [逐项复核](07-requirements-review.md#文章八条同序号复核)。此前内联 `awk` 计数命令的实际结果如下：

| 输入 | 实测行数 | 实际退出码／判定 |
|---|---|---|
| 200 行，有末尾换行 | 200 | 0／通过 |
| 201 行，有末尾换行 | 201 | 1／不通过 |
| 200 行，末行无换行 | 200 | 0／通过 |
| 201 行，末行无换行 | 201 | 1／不通过 |
| 本仓库 AGENTS.md／CLAUDE.md | 7／23 | 分别为 0／通过 |
| AGENTS／CLAUDE 入口模板 | 7／28 | 分别为 0／通过 |

本次未新增或安装自动 Hooks／CI 检查；200 行已经是 Skill 交付的必检条件，但不能称为已部署的自动门禁。未验证实际宿主局部规则加载、跨会话记忆效果及 30 秒阅读效果，也未推送或合并 PR。

同日按用户要求将第 1 条精简为约束与脚本调用，新增 `scripts/check-entrypoint-length.py`。4 项 CLI 测试覆盖 199／200／201 行、LF／CRLF、末行无换行、多文件与嵌套空格路径、读取错误和无参数；脚本不改写输入。本仓库入口实测仍为 7／23 行；完整 verify、76 项测试、Skill 格式和 diff 检查通过。未安装新 hook。

同日补充 [完整输入／输出示例](../../skills/documentation/agent-entrypoints/examples/confirmed-project.md)：成品由长度脚本实测为 32 行，Skill 格式、完整 verify、76 项现有测试及 diff 检查通过。示例是明确标注的虚构项目，未执行其业务测试或宿主加载；其余优化建议仅作审阅，未扩展实现范围。

## r6 规则清理与证据补充（2026-09-27）

工作目录为本仓库根目录，使用已有 `.venv`；以下命令均实际执行，退出码均为 0：

| 检查 | 结果与覆盖 |
|---|---|
| `bash scripts/verify.sh` | 76 项测试、结构／路由和 full 文档审计通过；无新增测试或执行脚本 |
| skill-creator 的 `quick_validate.py` 分别检查 agent-entrypoints、living-docs-governance | 两个 Skill 格式有效；不证明实际 Agent 行为 |
| `python3 scripts/check-entrypoint-length.py AGENTS.md CLAUDE.md skills/documentation/agent-entrypoints/examples/agents.example.md` | 分别 7、23、32 行，全部通过 |
| `git diff --check` | 无空白错误 |

人工核对根 AGENTS 指向 CLAUDE，后者未反向要求加载 AGENTS；文章来源、Skill、示例和产品主记录的引用可达。清理依据及命令未运行等场景见 [r6 复核](07-requirements-review.md#r6-规则清理与证据复核2026-09-27)。CONTEXT 缺失仍属按需载体，不补空壳。

本次只改规范与示例，未对业务项目执行规则删除，未验证真实宿主加载、跨会话效果或统一 setup；未新增 Hook、推送、合并或发布。

## r7 统一 setup 验证（2026-09-28）

对应 TEST-INIT-001、TEST-SETUP-001 与 GSU-1—GSU-5。修复基于本地产品能力工作区，尚未提交、推送或合并，不沿用旧 PR HEAD 的 CI 结果。

| 实际输入 | 生成与保留结果 | 第二轮入口行数 |
|---|---|---|
| 新项目：读书摘记，只有目标和范围 | 新增产品入口、十阶段资料及 AGENTS；原 README 不变，需求草案和未知技术栈明示 | 9 |
| 已讨论：值班换班工具，有已确认规则和验收条件 | 新增产品空间与 AGENTS；原讨论不变，PRD 阶段只映射原主记录，消息提醒仍待确认 | 10 |
| 已有代码：班次导出器，已有 AGENTS、SHIFT-7 r2、测试与 hook | 新增 11 份产品文件并增量更新 AGENTS；原规格、源码、测试、hook 的 SHA-256 不变 | 15 |

三个项目合计新增 35 文件，修改 1 份已有入口，删除 0；建档后共有 42 份项目文件。首轮入口 10／11／16 行；发现单次权限混入常驻规则后，仅修三份入口，并复验以下项目：

- 在各隔离项目根执行 `python3 <插件目录>/scripts/audit-docs.py --root <该项目根> --scope full`：三次退出码均为 0，本地链接和 docs 可达性通过。使用完整绝对目标根，没有误审插件仓库。
- 将三份实际 AGENTS 传入 `check-entrypoint-length.py`：退出码 0，分别为 9／10／15 行。
- 在 existing 根执行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py'`：退出码 0，既有 1 项测试通过；只覆盖空记录输出，不是完整业务验收。
- 两轮重复 existing setup、随后只读探测：各轮前后路径与 SHA-256 均完全一致，增改删为 0。未访问 Tracker，未安装或修改 hook，未创建 Git 历史、提交或推送。
- 补充权限负例：另一个尚未配置的项目只有 README，明确要求“先给建议、不写入”；Agent 提出了 12 个拟新增文件但未落盘，执行前后仍只有原 README，SHA-256 相同，增改删为 0。没有用已配置项目的无改动替代确认门验证。

AGENTS 主源布局未预建 CLAUDE 四件套，full 审计因此保留缺失可选脊柱、无 Git／LOG 历史、CONTEXT／ADR 未启用等未验证提示；没有为消提示制造空文件。每份阶段文件记录真实状态与缺口，不把目录齐全当成调研、开发或验收完成。隔离样例与原始命令输出保留于本次执行的临时证据目录，不进入插件包。

仓库根使用既有 `.venv` 执行 `bash scripts/verify.sh`：76 项测试、路由结构、full 审计通过；4 个相关 Skill 的 `quick_validate.py`、`git diff --check` 均通过。本仓库 AGENTS／CLAUDE 实测 7／25 行，模板 7／28 行，完整入口示例 32 行，长度检查均退出 0。

未验证：Claude Code 原生 slash command／角色调度、Codex 跨会话自动加载、hook 事件、真实业务项目接入和业务验收。上述结果是共享 Skill 的实际 Agent 执行加确定性检查；不是纯文本审查，也不等于已部署或已发布。

## pre-push 安装修复（2026-09-28）

TEST-PR-001 新增 3 项安装回归：旧分支与 linked worktree 的真实 push 成功，坏文档仍被拒绝；已有 hook 默认不覆盖，明确替换时备份；支持外部 hooksPath，拒绝工作树内路径。先用旧包装器复现缺脚本失败，再用稳定运行快照通过。仓库根 `.venv` 下执行 `bash scripts/verify.sh` 全部通过，共 79 项测试。本仓库失效包装器已在备份后替换；未替其他项目安装，也未改变远端保护规则。

## PH-20261011：项目健康采集实跑

本轮在既有 agent-workflow-governance 增加项目健康附件和静态采集器，未新增 Skill、安装 Waza、检查全局配置或会话历史。用户要求完成本项目实跑和独立复核，不提交、不推送。采集器只输出候选，文档审计另行复用既有脚本。

项目实跑证据保存于忽略目录 .governance/project-health.json 与 .governance/project-health-doc-audit.json。采集确认项目指令和 CI 字面引用同一 scripts/verify.sh，audit-cheap 的变量路径作为待人工核对项；旧审计回执即使 HEAD 相同也保持未验证，静态采集不证明 CI 已运行或项目整体健康。

独立复核发现并已修正：git status 可触发 clean filter，rev-parse 可加载项目外 Git config include；因此完全去除 Git 子进程，只读取受限本地 refs，不支持的 Git 布局明示缺口。另修复复合命令的空壳误判、显式会话目录回执读取以及 CLI 空格／引号凭据脱敏。专项 15 项回归通过；独立 Agent 复测原故障 fixture、项目实跑和新测试后确认受检范围无剩余阻塞。当前项目全量 108 项单元测试通过，diff 格式检查通过。独立原始回执保留于 /tmp/health-independent-final-tests.log、/tmp/health-independent-final-recheck.json、/tmp/health-independent-final-include.json 与 /tmp/health-independent-final-project.json。采集结果为 9 个源文件、37 条候选命令，1 项动态路径解析缺口；HEAD 为 fe0643a，未提交或推送。

完整工作区验证曾因另一任务新建 docs-audit 尚未接通 README 和总路由失败，两项均不属于本轮改动；不替该任务注册或删除 Skill。环境、范围和并行改动导致的验证差异分别记录，不覆盖失败。

### PH 提交隔离

2026-10-11 阿磊授权仅提交本次项目健康采集，不推送。以 fe0643a 为基线隔离：工作区中的 agent-workflow-governance 尚未提交，因此把本次采集附件与路由接到已提交的 living-docs-governance，不带入其他 Skill、拆分或迁移。上文 108 项和独立复核属于实施工作区；隔离快照的验证单独记录。

隔离快照保留基线 10 个 Skill，使用项目原路径 .venv 完整 verify 通过，共 100 项测试（含 15 项健康采集回归）。采集器与测试和独立复核版本逐字一致，仅调整所属 Skill 的入口与附件路径。原始回执：/tmp/health-isolated-verify.log、/tmp/health-isolated-tests.log。未推送、未运行远端 CI。

### PH 接入最新 main

用户随后授权创建并合并 PR。以 1f7ae10 为基线，仅移入 afa3d87 的健康采集功能，排除其父提交 fe0643a 的治理和环境修复；保留 main 已合并的 Skill 与历史记录。采集器和 15 项回归保持原样，入口继续复用 living-docs-governance。

最新 main 基线上的独立 PR 工作区使用项目 .venv 验证：完整 verify 及 106 项单元测试通过（包含本次 15 项）；原始日志为 /tmp/health-pr-verify-final.log 和 /tmp/health-pr-tests.log。此前 100 项与 108 项分别属于不同快照，不能作为此次 PR 的测试数量。

### PH：PR #40 评审修复

来源为 [合并后独立评审](https://github.com/qshanx/docs-governance/pull/40#issuecomment-6109666108) 及阿磊本会话的修复要求。两类 P2 已用新增 fixture 复现：常见脚本入口漏采／CI 对应缺失，以及环境前缀命令误判空壳。4 项新增参数化测试在修复前出现 11 处断言失败；修复后健康采集专项 20 项全部通过，包含既有不执行、越界、旧回执与脱敏检查。修复只扩展静态识别并保守标注缺口，没有引入 Shell 执行或完整 YAML 解析。回执独立指纹为后续建议，本轮未实施；原生宿主调用验收仍未执行。

项目实跑补查后增加第 5 项回归，防止 unittest 的筛选文件名和 GitHub .sha 字段被识别成脚本；脚本路径仅从调用位置取值。该版本实跑为 19 个源文件、63 条候选，4 项复杂引号／动态路径解析缺口，collection_changed=false；这些缺口不代表命令执行失败。

## MOD-20261011：模块治理与链接检查

阿磊确认将模块流程独立为 module-governance，并按任务意图触发。实现复用入口、领域上下文、契约与架构 Skills；普通 Bug 不建档，纯审计不写入。实际样本、相对路径误报纠正与生成后链接检查见[实跑记录](../audits/2026-10-11-module-governance-real-run.md)。样本通过不等于全宿主命中率保证；未迁移真实业务项目。

独立提交以远端 main 的 `1b07eb2` 为基线，不带入本地主工作区的其他改动；保留上游现有路由、维护及审计流程。使用项目已有 .venv 执行完整 verify：112 项测试及文档审计通过。早先实跑报告的 109 项属于当时混合工作区，不作为本提交测试数量。

### MOD：PR #46 新评审与最新 main 集成

按 [PR #46 新评审](https://github.com/qshanx/docs-governance/pull/46#issuecomment-6110080987) 修正两项 P2：根入口或架构主记录充分覆盖模块时标复用，不因没有局部文件报缺口；contract-first 按进程内与网络边界区分验证要求。ARCHITECTURE 同步模块编排与决策载体选择。普通 merge 接入 `0b6573d`，逐段保留双方路由、说明与测试记录。

新隔离会话显式使用 docs-audit 与 contract-first，读取实际库存／价格样本的 7 个文件并运行 2 项测试，均通过。实际输出认可根入口和共享 CONTEXT 的覆盖；进程内调用不要求网络序列化，价格接口已有真实 JSON bytes 证据但仍指出缺标准 schema 校验和 HTTP 联调。样本 7 个文件的 SHA-256 前后一致。该测试验证规则分支与只读行为，不代表隐式触发或完整业务验收；原始会话记录在 `/private/tmp/pr46-review-events.jsonl`。

在最新 main 集成工作区激活已有 .venv 后，完整 `bash scripts/verify.sh` 退出 0：114 项单元测试、插件结构、引用与 full 文档审计通过。提交快照检查、远端 CI 和合并状态以其后实际回执为准。

## AWG-PLACEMENT-20261011：规则落点检查实跑

当前混合工作区按新增附件完成只读诊断，范围、证据和建议见[实跑报告](../audits/2026-10-11-governance-rule-placement.md)。文本场景核对覆盖已有 Skill 复用、项目事实不转通用 Skill、单次故障不泛化、已有脚本缺调用与只读停止。AGENTS／CLAUDE 分别 7／26 行，长度检查通过；未安装 Hook、修改门禁或调用原生宿主自动事件。历史审计只登记 Issue #43。

### AWG-PLACEMENT 提交隔离

以 main 的 1b07eb2 为基线，单独提取规则落点附件、实跑报告及必要登记。agent-workflow-governance 的广义框架尚未进入 main，本 PR 沿用该名称但仅提供本次只读检查的最小入口；未带入上下文／工具／隔离治理附件、其他未提交 Skill、治理修复、脚本或 Hook 改动。原实跑属于混合工作区，不能当成本次隔离快照的验收。

## r8：技术文档表达（2026-10-05）

> 2026-10-11 调整：下文保留原方案与试验记录；当前改为引入 [writing-for-agents](../../skills/documentation/writing-for-agents/SKILL.md)，保留 MIT 许可证、固定来源与本地含义核对。旧试验不代表新 Skill 已通过行为验证。

对应 TEST-WRITING-001 与 TWR-1—TWR-5。基于主分支 `520696eb519f2dd50531ba91abe5ad89478ffdf3` 的真实文档副本；新增规则独立整理，未安装新依赖、Hook 或宿主 Agent，未执行指南中的业务命令。

| 实际场景 | 执行与核对结果 |
|---|---|
| 中文操作指南：`references/document-policy.md` 的隔离副本 | 执行 Agent 从总路由定位新 Skill 并读取包内规则，改写长句、条件和失败分支。独立审阅者逐句对照，未发现语义漂移 |
| 合成发布约定：推荐测试、数据库备份、文档豁免、回退计划和缓存例外 | 保留“最好”“只有……才必须”“不需要”“尚未验证”“计划”；缓存为空的条件仍覆盖成功和缺失两分支，读取先于重建 |
| 英文 `CONTRIBUTING.md` 的只读副本 | Agent 从活文档委托读取新 Skill，返回四处可粘贴建议，另列事实疑点；原文与结果字节一致，SHA-256 均为 `5c29068e65b9a6786a2402e509bcf459680bbfe2e852eb8a00c75754a1e2bbb2` |

实际改写片段：

> 原文：目前尚未验证自动回退，下一版本计划支持它。
>
> 改写：目前尚未验证自动回退，下一版本计划支持自动回退。

只明确代词，不改变证据或完成状态。两份改写产物的标题、列表编号、代码块、行内代码、链接目标和数字序列与原文逐项一致；这些机械比对与独立语义审查分开进行。指南输出 SHA-256 为 `1f4895e7837a41ce9cb546cd5859600eaef39871a59b64b0e6d17b6b0f201198`，合成样例输出为 `bd1ecd4e8ac3756ada198c111a76669bb1f6126aa7ad642cd36be4300e7beca9`。临时输入、原文副本和产物保存在本轮本地证据目录，没有将改写指南或 CONTRIBUTING 混入插件改动。

| 实际检查 | 结果与覆盖 |
|---|---|
| 激活已有 `.venv` 后运行 `bash scripts/verify.sh` | 退出码 0，79 项既有单元测试、11 个 Skill 的路由／说明、Python 编译和 full 文档审计通过 |
| `quick_validate.py` 检查 technical-doc-writing、docs-governance、living-docs-governance、agent-entrypoints | 四个 Skill 均有效；格式检查不代替行为验证 |
| `check-entrypoint-length.py` 检查本仓库 AGENTS／CLAUDE 及两个入口模板 | 全部退出 0；分别 7／26 行及 7／29 行 |
| `bash -n scripts/verify.sh`、`git diff --check` | 均退出 0 |
| 实际引用检查段的临时夹具 | 根引用与包内引用齐全时退出 0；包内文件或整个 reference 目录缺失且根目录同名文件存在时均退出 1；根引用缺失且包内同名文件存在时退出 1 |

full 审计中的 CONTEXT 缺失是现有按需载体提示，本轮不补空壳。提交后 `check-pr-docs.py --base origin/main` 与远端 CI 须检查实际提交，不能预先由本记录宣称通过。

验证边界：上述结果是实际 Agent 显式读取共享 Skill 后的执行及独立审查，不是宿主安装后自动选择 Skill 的证明。Claude Code 原生调用、Codex 跨会话发现、业务项目效果和标准合规未验证；本轮未合并、部署或发布。

## SETUP-20261012：补齐 #33 遗漏流程

以 main 的 `29f60c6` 为基线，只提取 #33 的首次建体系流程、三个参考文件及必要说明；分类和 docs-retro 已由其他 PR 合入，不重复引入。逐段核对保留项目健康采集、writing-for-agents、普通／兼容审计分流；模块治理及脚本、测试、插件加载配置未改动。

独立 Git 夹具使用 `audit-docs.py --root <目标根> --scope full` 实跑：未采用 LOG 返回 0；策略要求 LOG 却缺失、断链、删除已提交 LOG 历史分别返回 1。四例运行前后项目文件哈希一致。该结果只验证检查器与日志约定的兼容性，不代表新版 setup 的 Agent 生成、宿主加载或自动触发已经通过；这些行为仍待试点。本轮完整 `bash scripts/verify.sh` 退出 0：114 项单元测试、插件结构、引用与 full 文档审计通过。提交快照与远端 CI 仍以提交后的实际回执为准。

## ENV-20261014：讨论文档提交检查

本轮对象为最新 main 2c79c4f 上的隔离讨论分支，只新增环境讨论稿和必要导航／产品／状态记录。使用主项目已有 .venv 运行本仓库 scripts/verify.sh，并在提交后运行 check-pr-docs.py --base origin/main；命令、退出码与提交版本在 PR 的 Evidence 留证。

上述检查只验证讨论文档提交的结构、引用、历史与快照，不验证尚未实施的环境治理流程。未做新 Skill 行为试跑、环境配置、业务测试、宿主安装或自动调用；原工作区的未提交草案不进入本 PR，不据此前隔离探索宣称本方案通过。
