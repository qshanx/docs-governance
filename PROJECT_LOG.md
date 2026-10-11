# PROJECT_LOG.md — 只追加（永不改旧行）

## [2026-06-23] init | 建立插件可发布底座：git 初始化 + LICENSE(MIT) + CHANGELOG + .gitignore(排 .DS_Store) + scripts/verify.sh（结构完整性自检，实跑通过）
## [2026-06-23] init | 给插件自身套精简版四件套（dogfood，用自己的方法论治自己）
## [2026-06-23] audit | verify.sh 首跑全绿：JSON 合法 / hook 可执行 / 命令→agent→skill/template/reference 无断链
## [2026-06-24] feat | 借鉴 @vincemask《.claude/ 组织指南》补 4 处：skill 加「渐进式采用路径（带下一级预警信号）」+「团队 vs 个人分层」；README 加「治理常见错误」表；docs-auditor 扩到也审 .claude/ 配置目录本身（死配置/CLAUDE.md过载/模糊命名/个人混团队）
## [2026-06-24] audit | audit-blog 真项目治理审计跑通（可信度低，揪出 STATUS 自相矛盾/旧快照、MAP 导航6→7、README 描述已删架构等 ~14 条）——第 4 个 dogfood
## [2026-06-28] feat | 新增 skill `loop-design-check`：把任务写成目标导向 loop（该不该建→可判定目标→回路类型→plan/build/judge 骨架）+ 体检 loop（五个崩法防呆+判断留人红线），防空转/作弊/跑飞。源自 vault《控制论×Loop×Goal》；机制层引用 ECC autonomous-loops/continuous-agent-loop 不重写
## [2026-07-02] feat | /governance-init day-0 骨架命令 + governance.example.md 模板（模板单源、瘦身三件、hook 交给插件 Stop、去悬空引用/去 Python 写死/去私有约定）；plugin 0.3.0，CHANGELOG 补 loop-design-check
## [2026-07-02] fix | verify.sh 修两伤：skills 断链漏检（MISS 正则 + 扫描范围扩到 README/使用说明/CLAUDE_MAP，三段测试证伪→证真）+ agent 白名单硬编码改动态"孤儿/未登记"检查；README 补市场安装命令+验收命令+真实审计样例；发布 v0.3.0
## [2026-07-02] governance | 方法论优化 backlog 五条立项（审计脚本化/pre-commit 固化/LOG 消费端/并发约定/文档复利三动作），方案细节见 STATUS Backlog
## [2026-07-02] feat | backlog #2 落地：templates/pre-commit.example 护栏（代码改动必须同批一行流水账；测试/文档豁免；--no-verify 后门）+ /governance-init 自动装 + /governance 询问装；临时仓四段测试全过（拦/带账过/豁免过/后门过）
## [2026-07-03] feat | 第三条线·模块回归审计首版：module-regression skill（台账三要素/审计五步/三铁律）+ regression-auditor agent（只跑只报不修）+ /regression-audit 命令（init 建台账草稿）+ REGRESSION.example 模板；plugin 0.4.0；未真项目实测，待经营报表试点

## [2026-07-03] feat | 吸收「熵与法典」九层判定思想：module-regression 加判定点清单+铁律4坑必下沉；governance-audit 改两段流水线（新增 scripts/audit-cheap.sh 便宜层先跑红了短路）；living-docs 加标准变更留痕+LOG蒸馏升级为蒸馏+复盘；新增 /governance-retro（LOG复盘统计→下沉候选）；STATUS 模板加审计保鲜度。修 audit-cheap.sh bash3 多字节变量名吞并 bug（$VAR后紧跟中文标点须${VAR}）。

## [2026-07-12] feat | 测试协作治理 v1：新增 test-collaboration skill + TESTS.example 模板，盘点现有测试并把需求/Bug 转成 TEST-ID；REGRESSION.md 改为只管下游与回归命令并引用 TEST-ID；plugin 0.5.0，待真实项目试点
## [2026-07-24] feat | test-collaboration 增加跨端契约测试链：同一机器可读契约驱动契约自身校验、消费者类型/mock 测试、提供方真实序列化验证和最小联调证据；TESTS 模板新增统一 TEST-ID 与证据表，不复制契约字段
## [2026-08-02] feat | 新增 Codex/ChatGPT 插件 manifest 与 AGENTS.md 薄桥接；共用现有 skills，补 Codex 直接调用、宿主 agent 降级、双端安装说明和 manifest 一致性校验
## [2026-08-02] feat | 文档治理 v0.7：新增总路由、CONTEXT/ADR、变更影响、五范围只读审计与 PROJECT_LOG 超 200 事件后的 Markdown 归档 + SQLite 可重建索引；12 个单测覆盖关键确定性行为
## [2026-08-13] docs | 面向公开试用补英文概览、三分钟只读审计路径与贡献模板；不新增方法论，外部协作仍以现有 Skill 为唯一源
## [2026-08-13] feat | CLAUDE_MAP 增加按需 Module 架构契约：权责与状态归属、代码依赖图和独立核心流转图，并接入治理、审计、变更影响与同步流程
## [2026-08-13] refactor | 根据评审将 Module 架构契约从 CLAUDE_MAP 下沉到独立 ARCHITECTURE.md；MAP 仅留导航，新增模板、审计载体检查与真实项目自治理示例
## [2026-08-13] test | 本插件首次建立 TESTS.md，记录测试资产、存在理由、6 个 TEST-ID 与缺口；修复 TEST-ID/删除区两类审计误报，15 个单测通过并接入 GitHub Actions
## [2026-08-13] audit | governance-init 在临时空仓完成 Codex 共享流程首跑与首提；Claude Code 原生命令仍待明确的数据出境授权
## [2026-08-13] docs | 重绘 diagram/architecture.svg 与 2x PNG，使双宿主、总路由、7 个专项 Skill、确定性执行和 Markdown 事实源与 ARCHITECTURE.md 一致
## [2026-08-14] docs | 明确 docs-governance 产品定位：把优秀 Agent 的一次性工作沉淀为可继承、可验证、可持续演进的项目集体能力；同步总路由、双语 README、使用说明和双端 manifest

## [2026-09-05] fix | 修复评审并发写回、删除区判定、日志基线与格式、引用式链接及可选载体审计；共享流程归 Skill，机器契约模板与开发验证接入；28 个测试通过，证据见 [本轮验证](docs/audits/2026-09-05-governance-fixes.md)
## [2026-09-05] governance | 标准变更：日志仅比较 HEAD → 提交审查必须指定基线；日志格式统一为带二级标题的事件；CONTRACT 手写字段 → 登记唯一机器契约；默认 verify 增加 full 审计与契约模板验证，原因是本轮已复现的漏检和双源风险
## [2026-09-05] audit | PR #3 修复提交 c132f0a 的 push 与 pull_request 验证均通过；记录远端证据并更新 CI 健康指标，见 [本轮验证](docs/audits/2026-09-05-governance-fixes.md)
## [2026-09-05] governance | 标准变更：指标越线或标准变更缺记录即 P0 → 依据实际影响和证据分级；STATUS 分开紧急风险与普通验证缺口，日志按有意义的结果留痕，减少数值误报和重复维护
## [2026-09-05] refactor | 日志审计与归档共用解析器；审计结果统一渲染文字/JSON，区分文档问题、未验证和执行错误；治理引用已有审查与运行证据，37 个测试通过，见 [架构优化验证](docs/audits/2026-09-05-shared-audit-results.md)
## [2026-09-05] fix | PR #4 双轴审查发现损坏 Git 被视为缺失、子项目历史路径不一致及循环链接中断 JSON；补 3 个回归并修复，远端基础提交证据与修复记录见 [架构优化验证](docs/audits/2026-09-05-shared-audit-results.md)
## [2026-09-05] fix | PR #4 复核补充父路径为普通文件的断链分类回归；按文档失败返回 1，循环链接仍按执行错误返回 2
## [2026-09-22] feat | 新增 product-evolution 与入口模板，按阿磊指定十阶段在 docs 下组织产品管理文件，接入路由、地图和同步；本轮验收与试点边界见 [产品管理](docs/product/README.md)
## [2026-09-22] governance | 标准变更：产品流程执行条件收窄为完整十阶段文档管理；经阿磊确认新增变更收尾审计和提交时文件归位约束，取消每日定时方案；位置配置与验证见 [护栏说明](references/document-policy.md)
## [2026-09-22] audit | 盘点登记的 11 个本地项目及常用开发目录的 37 个仓库目录，补充只读接入适配评估；发现全文件指纹、根定位、历史告警与路由误报等推广障碍，未改业务项目，证据见 [跨项目评估](docs/audits/2026-09-22-cross-project-feasibility.md)
## [2026-09-22] feat | 经阿磊确认新增 PR 前强制扫描：pre-push 与 PR Actions 对提交快照执行同一审计，按项目变更映射列出关联文档；10 个集成测试覆盖真实 push 拦截与修复、子目录、worktree、原始基线及工作区隔离，全套 64 个测试通过，见 [护栏说明](references/document-policy.md)
## [2026-09-23] feat | 经阿磊确认新增 product-docs-manager 产品文档管理员角色，复用现有 Skills；六类资料映射到原有十阶段，补充来源登记、稳定需求编号、修订及授权边界，不改业务项目；范围与文本审查见 [产品管理](docs/product/README.md)
## [2026-09-23] fix | 按 PR #12 独立评审修复 Stop 子目录静默漏审：统一显式根、Git 边界内最近配置及旧四件套定位，未知根明确提示；新增 8 个回归，全套 72 个测试及 verify 通过，验证范围见 [测试记录](docs/product/09-test-release.md)

## [2026-09-23] feat | 产品能力规格 r3：PM 四类材料与既有六类记录、十阶段共用主记录；CLAUDE／模板触发按任务读取，Skill 管局部读取、依赖补读与分批审查。文本场景已复核，真实上下文效果待试点。
## [2026-09-27] feat | 新增 `/governance-setup`：已有项目首次接入先只读探测既有真相源、Tracker、hooks 与验证入口，展示最小草案并在确认后写入；与空项目初始化和日常维护入口分工，命令适配完整性进入 verify。
## [2026-09-27] fix | 修正首次接入入口规则：保留 `CLAUDE.md` 为 Claude 事实源；Codex／跨宿主项目经确认可产出只桥接它的薄 `AGENTS.md`，并把此情景加入 TEST-SETUP-001。
## [2026-09-27] feat | 按 ENP-20260927 新增 agent-entrypoints 与 Vince 文章摘要，入口规则由项目证据生成并衔接 PRD／Spec；标准从无条件 AGENTS 薄桥接调整为沿用已确认共享主源、按宿主能力适配，原因是 AGENTS 可为完整入口且 Claude 已有条件支持；本仓库主源不迁移。旧 setup 范围已被后续要求纠正，统一编排与 PR 合并仍未完成，见 [能力规格](docs/product/06-prd.md)。

## [2026-09-27] governance | 标准变更：入口长度仅作复核信号 → 每份 AGENTS.md／CLAUDE.md ≤200 行硬验收；依据阿磊后续明确纠正，同步规范、模板与产品验收，并按文章来源 1—8 补齐具体执行和逐项检查。此为治理规则，不是宿主解析器截断或已安装自动门禁；见 [入口规范](skills/documentation/agent-entrypoints/SKILL.md)。

## [2026-09-27] fix | 按阿磊要求将入口长度规则收紧为一句约束与脚本调用，新增只读计数脚本及边界测试；200 行标准不变，不安装新 hook，见 [入口长度检查](scripts/check-entrypoint-length.py)。

## [2026-09-27] docs | 新增 Skill 内的完整项目输入与 AGENTS.md 成品示例，明确虚构案例和验证边界，正文仅挂按需链接；其余规范精简和验证建议仍属审阅意见，未实施，见 [示例](skills/documentation/agent-entrypoints/examples/confirmed-project.md)。

## [2026-09-27] docs | 按阿磊要求建立 [Issue #15](https://github.com/qshanx/docs-governance/issues/15) 跟踪 Agent 入口规范，置顶文章来源并关联 #11、#10 与 setup PR #14 背景；同步产品索引，优化建议仍待确认，未推送本地实现或合并 PR。

## [2026-09-27] governance | 标准变更：入口经验更新与验证摘要 → 补充有依据的旧规则清理及命令工作目录／退出码等交付证据；依据阿磊对 Tw93 适配建议的确认，同步示例和现有 setup 探测／Skill 调用顺序，文章链接与本地验证结果已回写 Issue #15。未新增 Agent／Hook，统一 setup 仍未完成；范围及证据见 [能力规格 r6](docs/product/06-prd.md#r6规则清理与交付证据) 和 [测试记录](docs/product/09-test-release.md)。

## [2026-09-27] governance | 按阿磊确认优化本仓库共享 CLAUDE 入口：补项目用途、验证工作目录／环境及 TESTS 路标、专项 Skill 路由；标准变更：正文中文且英文仅限触发词 → 治理正文默认中文，保留现有英文文档及代码标识／技术术语，消除与英文 README 的冲突。AGENTS 薄桥接和共享主源不变，不修改通用模板或其他 Skill。

## [2026-09-28] fix | 按阿磊对 PR #14 审阅结果的“修复”确认，统一新项目、讨论后项目与已有项目的 setup；docs-governor 按共享 Skill 编排产品文档和 Agent 入口。标准变更：init 独立流程并默认 Git 首提／装 hook → setup 唯一流程、init 兼容别名，Git 与 hooks 须明确授权；原因是旧骨架无法承接产品文档包且两入口职责重复。范围见 [能力规格 r7](docs/product/06-prd.md#r7统一-setup-编排)，本地验证与远端边界见 [测试记录](docs/product/09-test-release.md)。

## [2026-09-28] fix | 修复 pre-push 随分支切换丢失脚本：新增显式安装器，将检查器及依赖固定到 Git 公共元数据，默认保留已有 hook、明确替换先备份；真实 push 回归先复现失败再通过，13 个 PR 集成测试通过。审计器复用同一忽略目录常量；安装与边界见 [护栏说明](references/document-policy.md)。

## [2026-09-28] fix | 将 PR #12 已提交产品能力整合到 PR #14，本地解决 6 份文档冲突并保留双方历史事件；统一 setup 与入口规范修复一并纳入，未混入作者名迁移及无关研究。远端推送与合并尚未执行。

## [2026-10-09] governance | 按阿磊“修复吧”确认落实 Issue #5 的接口变更切片；标准变更：按映射提醒核对 → 在共享 change-impact 中按固定版本、事实差异及引用补查正文，给出位置、依据和无需更新理由。活文档审查引用该流程，增加可复跑样例；本地验证与已知场景边界见 [TEST-IMPACT-001](TESTS.md#test-impact-001事实变化后的文档核对)，更广事实类型及业务试点仍由 Issue 跟踪。

## [2026-10-10] docs | 按阿磊确认，将架构文档的必要性判断、生成与审查独立为 [architecture-docs](skills/documentation/architecture-docs/SKILL.md)；活文档治理改为委托，入口登记同步。先判断需要新建、沿用、暂不需要或证据不足，区分实际结构、确认设计与建议；不拆其他治理流程。

## [2026-10-10] governance | 接通模块变更的影响分析、实际 diff 对照、下游回归与文档同步；入口只留路标。增加带来源的文档候选检索和审计失败短路；未配置台账时复用真实依赖与现有测试。范围及验证见 [TEST-IMPACT-001](TESTS.md#test-impact-001事实变化后的文档核对)。

## [2026-10-10] test | 日常维护增加受影响示例与命令的执行验证；复用接口合成样例，直接读取文档原文验证旧调用失败、只修文档后通过、内部重构保持有效及错误输出反例。仅在临时副本执行，边界与命令见 [接口样例](skills/engineering/change-impact/examples/interface-change.md#示例与命令验证)。

## [2026-10-11] docs | 精简 [日常文档维护](skills/documentation/docs-maintenance/SKILL.md) 为确认变化、定位并更新说明、验证交付三步；把维护范围与完成要求放回对应步骤，保留需求冲突、历史语义、旧证据复验及文档原文示例验证，不改变其他 Skill 或检查实现。

## [2026-10-11] docs | 精简 docs-maintenance 三步交接：明确行为变化、影响对象及依据；优先复用影响分析，不足时补查候选，由维护 Skill 判断并更新正文；历史留痕沿用项目主源，LOG 不默认新建；集中验证与交付条件，保留判断表及示例验证。

## [2026-10-11] docs | 将 docs-maintenance 的借鉴来源移至 PR #29 描述保留溯源，Skill 仅保留执行所需流程与案例链接；维护行为不变。

## [2026-10-11] docs | 根据 PR #29 评审澄清有效影响分析的复用条件：覆盖当前范围、版本与未提交变化，并包含适用审计结果；新变化、失败或未覆盖项需补查，不沿用旧结论。其余维护流程不变。


## [2026-10-10] docs | 按阿磊要求及 writing-for-agents 重整 [Agent 入口 Skill](skills/documentation/agent-entrypoints/SKILL.md)：先核对事实、判断内容用途与放置位置，再组织入口并逐项验收；精简描述和重复解释，示例补充事实到内容的取舍。保留八条编号、每份入口 200 行及既有授权、主源和证据要求。


## [2026-10-10] docs | 根据独立入口试验补强 [Agent 入口 Skill](skills/documentation/agent-entrypoints/SKILL.md) 第 4、6 条：用典型任务沿指针核对正文与实现，自动化触发与执行状态查配置和运行证据，避免只查断链或固化易过时状态。试验材料留在业务仓库外，本次未修改正式业务入口、安装 Hook 或增加检查脚本。


## [2026-10-10] docs | 精简 [Agent 入口 Skill](skills/documentation/agent-entrypoints/SKILL.md) 前置流程：明确生成／优化／审查任务，从已确认对话和项目资料获取依据，再按八条规范处理与交付；删除重复的常驻内容分配表和分散完成条件，八条规范及按需参考保持原样。


## [2026-10-11] docs | 调整 [Agent 入口 Skill](skills/documentation/agent-entrypoints/SKILL.md) 第一步：结合相关项目文档与已有对话了解项目，移除“没有对话才读文档”的条件；配置和验证命令按需查实际项目，其余步骤与八条规范保持不变。


## [2026-10-11] docs | Agent 入口流程精简为阅读、合并、逐段取舍、补齐检查四步；八项规范下沉至 [独立参考](skills/documentation/agent-entrypoints/entrypoint-standards.md)，执行时明确读取。优先合并到 AGENTS.md，保留独有有效规则并更新引用后删除旧入口；逐段检查全部受检入口，避免遗漏主文件中的冗余说明。已知 SaaS 案例用于复核，业务项目文件不包含在本次提交，宿主加载效果未验证。


## [2026-10-11] docs | 根据 PR #21 复审统一入口主源选择：保留既定主源，无既定主源时优先 AGENTS.md，已有迁移授权直接沿用；迁移保留宿主专属约束并核对加载方式。同步八项规范措辞并清理末尾空行，使用提交范围检查验证格式。


## [2026-10-11] docs | 将 main 已有 Skill 按文档管理与工程分类，预留试验与废弃目录；同步双端加载配置、引用及目录检查，不合入其他功能 PR。历史仅更新 Git 可识别的迁移链接。

## [2026-10-11] fix | PR #29 及依赖接入分类后的 main，保留最新三步维护流程、影响分析复用条件和示例验证；统一旧同步入口委托与架构主记录选择，历史按项目既有主源记录。

## [2026-10-11] fix | 分类合并时从真实提交重命名补足历史链接迁移依据，处理先精简后移动导致的相似度丢失；仍拒绝日志正文、链接文字、锚点及无关目标改写。

## [2026-10-11] docs | 将 PR #32 已确认的 docs-retro 独立集成到 main：复盘文档管理经验，给出具体落点、修改草稿与验证办法；同步调用入口，不引入原目标分支的其他功能。
