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
