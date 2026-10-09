# 接口变更的文档核对场景

合成样例来自 [Issue #5 的实测](https://github.com/qshanx/docs-governance/issues/5#issuecomment-6075874052)。方法只在 [change-impact](../SKILL.md#按事实核对文档) 维护；本页给出输入和验收口径，不是业务项目事实或自动语义检测器。

## 准备与执行

从插件根目录运行 [样例生成器](../../../tests/fixtures/document-impact.py)，目标必须是不存在的目录：

```bash
python3 tests/fixtures/document-impact.py /tmp/document-impact-run/api --case interface
python3 tests/fixtures/document-impact.py /tmp/document-impact-run/internal --case internal
```

复跑使用新的目标目录。输出 JSON 提供各样例的 root/base/head；只在隔离样例创建本地 Git，不安装 hook、不访问远端。字段与实现一起变更，回执由实际序列化输出生成并绑定输入哈希；示例不启动 HTTP 服务。

给执行审查的 Agent 只提供下列任务及对应 JSON，不提供下方验收清单：

> 按 change-impact 的“按事实核对文档”，只读审查此样例的 base/head 变化。先执行插件的 PR 文档检查，再对同一提交快照进行语义核对；给出具体文档位置、依据、需要更新或无需更新的理由，以及未验证项。不要修改样例，也不要把脚本通过当作语义通过。

先运行 `python3 <插件目录>/scripts/check-pr-docs.py --root <root> --base <base> --head <head>`；非零按审计规则先处理。确定性检查可能报告未采用可选载体，不因此补造文件。语义审查使用实际 diff 与文档上下文。

## 验收清单（审查完成后对照）

| 场景 | 应观察到的行为 |
|---|---|
| interface：映射内未改说明 | 指出 `docs/api.md` 的旧调用与新订单契约冲突 |
| interface：映射内已改说明 | 同样指出 `docs/consumer.md` 的旧调用，不能被新增说明掩盖 |
| interface：映射外说明 | 沿契约引用或旧标识定位 `docs/integration.md`，注明候选来源 |
| interface：重复决定 | 指出 `docs/faq.md` 复制当前决定；以 `docs/decision.md` 为主记录，建议 FAQ 引用 |
| 两例：反例 | `docs/reference.md`、`docs/history.md`、`docs/inventory.md` 无须改写，分别给出引用有效、历史用途和接口不同的依据 |
| internal：内部修复 | 对外响应与契约不变，无需改写调用说明或制造文档 diff |
| 两例：证据 | 复用 TESTS 与 LOG 指向的同一原始回执；区分输入哈希、执行观察与业务验收 |

记录样例 base/head、Skill 修订／哈希、Agent 与执行方式、具体发现及反例、遗漏／误报、实际读取／修改范围和耗时（未计时则未知）。同一 Agent 已参与构造或读过答案时必须注明“已知场景复核”，不能宣称盲测、稳定检出率或真实项目效果。

自动回归入口为 `python3 -m unittest tests.test_pr_docs.DocumentImpactFixtureTest -v`；它验证样例能复现失败形状及确定性护栏边界，不替代上述 Agent 审查。实际记录从 [测试台账](../../../TESTS.md#test-impact-001事实变化后的文档核对) 进入；跨项目只读试点仍需单独验证。
