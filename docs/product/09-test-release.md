# 测试上线

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

同日补充 [完整输入／输出示例](../../skills/agent-entrypoints/examples/confirmed-project.md)：成品由长度脚本实测为 32 行，Skill 格式、完整 verify、76 项现有测试及 diff 检查通过。示例是明确标注的虚构项目，未执行其业务测试或宿主加载；其余优化建议仅作审阅，未扩展实现范围。

## r6 规则清理与证据补充（2026-09-27）

工作目录为本仓库根目录，使用已有 `.venv`；以下命令均实际执行，退出码均为 0：

| 检查 | 结果与覆盖 |
|---|---|
| `bash scripts/verify.sh` | 76 项测试、结构／路由和 full 文档审计通过；无新增测试或执行脚本 |
| skill-creator 的 `quick_validate.py` 分别检查 agent-entrypoints、living-docs-governance | 两个 Skill 格式有效；不证明实际 Agent 行为 |
| `python3 scripts/check-entrypoint-length.py AGENTS.md CLAUDE.md skills/agent-entrypoints/examples/agents.example.md` | 分别 7、23、32 行，全部通过 |
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
