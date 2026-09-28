# AGENTS.md — 设备借用台账

## 项目

为小团队登记办公设备借出、归还。首版单机离线使用，不包含采购和财务核算。
技术栈：Python 3.12、Flask、SQLite；本文件是项目共享规则主源。

## 代码位置

- 业务代码：`src/asset_lending/`；页面模板：`src/asset_lending/templates/`。
- 测试：`tests/`。新功能代码与对应测试分别放入这两个位置。
- 查找非显然路径或新建／删除／重命名文件前，读 `CLAUDE_MAP.md`。

## 约束与验证

- 保持单机离线部署，不引入 Redis、MySQL 或外部 SaaS；持久化沿用 SQLite。
- AGENTS.md／CLAUDE.md 每份 ≤200 行，细节下沉；修改后按已安装的 agent-entrypoints Skill 调用长度检查脚本。
- 修改实现后，在项目根目录激活已有 `.venv`，运行 `python -m pytest -q`；失败先定位修复，交付报告实际结果。
- 当前未配置自动测试 Hook，以上检查须主动执行；未执行时说明未验证。

## 按需读取

- 变更需求、实现或验收前 → `docs/product/README.md`，定位当前基线，再读取 `docs/product/06-prd.md` 中的适用条款。
- 跨模块设计或改变依赖方向前 → `ARCHITECTURE.md`，核对现有边界。
- 选择测试范围或排查测试失败 → `docs/testing.md`。
- 处理曾经解决过的问题 → `docs/working-notes.md`，只读相关经验，不全量加载历史。

## 协作与经验

- 中文沟通，先给结论，再给改动、验证命令／工作目录／退出码及未验证原因。
- 任务收尾时，将含适用条件和证据的已复验经验更新到 `docs/working-notes.md`；按依据合并重复项、清理入口过时规则，保留有效红线，依据不明时标待核实；只读任务仅报告建议。
- 推送须用户明确要求，不因代码或测试完成而自动推送。
