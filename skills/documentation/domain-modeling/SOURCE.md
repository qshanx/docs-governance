# 来源与本地适配

- 上游：[Matt Pocock / skills — domain-modeling](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/domain-modeling)。
- 固定提交：`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`；引入日期：2026-10-12。
- 授权：[MIT License](LICENSE)，Copyright (c) 2026 Matt Pocock；完整授权随包保留。
- 本地已安装三份文件的 Git blob 与该上游提交一致：SKILL `9b97707e19ef1f590aada356f2b3f6bb881f91be`，CONTEXT-FORMAT `79bbb32f6fda55758b377c980f72a6cb2b8c670e`，ADR-FORMAT `d7e61f30a9fd8ca70d9ee68f019c2a9ebf2d13f7`。
- `CONTEXT-FORMAT.md`、`ADR-FORMAT.md` 保持上游原文；`SKILL.md` 仅在末尾增加本地适配与来源指针。文件名保留上游拼写，方便逐字核对。
- `project-adapter.md` 是本项目补充，不是上游方法；兼容入口 `context-and-decisions` 不再维护另一套建模正文。用户无需额外安装 Matt 插件。

该提交使用 CONTEXT 命名，与当前项目布局匹配。上游 main 在核对时使用 GLOSSARY 命名，不自动跟随升级；升级时比较固定提交并核对主记录路径，避免生成第二份词汇表。
