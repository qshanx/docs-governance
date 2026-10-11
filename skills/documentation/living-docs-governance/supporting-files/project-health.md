# 项目健康证据采集

用户要求检查项目健康、验证入口或 CI 衔接时读取。本流程只检查目标项目，复用入口规范、测试协作与文档审计，不新增 Skill，也不采集全局配置、个人记忆或会话历史。

## 执行

1. 明确目标根与范围：采集器只支持当前工作区。审查提交时，在对应独立快照执行，不把工作区结论用于提交。保留其他任务改动。
2. 用插件脚本采集静态证据：

   ```bash
   python3 <插件目录>/scripts/collect-project-health.py --root <目标项目根>
   ```

   只读根目录 AGENTS、CLAUDE、README、TESTS、Makefile、package.json、GitHub Actions，以及命令引用的项目内脚本。显式提供项目内 JSON 验证记录时追加 `--evidence <项目相对路径>`；不自动扫描日志或猜测历史记录位置；即使显式传入，也拒绝 `.codex`、`.claude`、`.agents` 内的文件。脚本不运行发现的命令，不访问用户目录，不安装依赖，不生成报告文件；stdout 为 JSON，由调用方决定是否在授权范围内保存。
3. 文档链接、ADR、TEST-ID 和历史完整性复用 `scripts/audit-docs.py`；此脚本由 Skill 另行按既有审计约定执行，不在采集器内复制或隐式调用。真实验证命令由当前任务授权和项目规则决定，不能因为静态发现而自动执行。
4. 核对证据：项目是否提供稳定验证入口，文档与 CI 是否引用同一脚本，脚本是否有真实检查逻辑。已有 `verify.sh` 不要求另建 Makefile。`same_literal_script_in_ci` 仅说明字面路径重合，条件、参数、工作目录、环境与运行状态需另核对。
5. 每项交付“证据路径／行号、版本与范围、问题或待核实项、影响、最小下一步”。引用 `test-collaboration` 和 `module-regression` 的验证规则；没有执行证据不能宣称健康、测试通过或覆盖充分。

## JSON 与边界

- `schema_version: 1`；`scope: project_worktree`；`git` 为可获得的 HEAD；dirty 明确不采集（避免 git status 触发项目 clean filter）。不启动 Git 子进程，仅读取项目内普通 `.git/HEAD`、refs／packed-refs；worktree 指针、共享元数据等布局标 unavailable，避免 Git 本地配置 include 导致越界读取；无 Git 时明确 unavailable，不强迫初始化。
- `files` 记录实际采集源文件的 SHA-256；`evidence_fingerprint` 只覆盖所列文件，不代表整个项目。`collection_changed` 表示复读发现采集中内容／Git 状态改变，此次证据应重采。
- `commands` 为候选及来源。`hollow_candidate` 是简单 shell／命令只打印或固定退出的启发式线索，需阅读确认；其他命令一律是未执行候选，不判有效或无效。
- `receipts` 只接收显式项目内 JSON；原结果与当前 root／HEAD 的比较是线索，记录始终标 unverified，不用相同 HEAD 或旧绿色日志背书当前工作区。历史记录引用已失效临时路径不自动判为当前故障。
- `coverage_gaps` 记录缺失、不可读、越界、符号链接和大小限制。根无效返回 2；完成采集返回 0，即使有候选问题或覆盖缺口，也不是健康通过码。
- 首版仅做轻量文本识别，不解析完整 Shell、YAML、Make 依赖图或 package 委托链，不检查嵌套入口与其他 CI 平台。动态变量、CI 条件、无匹配命令、外部路径都需要人工确认；不根据文件数量打分。

方法参考 [Waza health](https://github.com/tw93/Waza/tree/main/skills/health) 的项目可维护性方向；本实现独立编写，没有引入其总采集器、全局配置与会话采集，也未安装第三方包。
