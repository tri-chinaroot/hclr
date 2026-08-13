# HCLR 采集协议规范（v1.0）

> 版本：1.0.0（2026-08-12）｜ 作者：tri-chinaroot ｜ English: [PROTOCOL.md](PROTOCOL.md)
>
> 本文档定义**如何在任意AI对话系统中持续采集HCLR数据**。它是方法论文（[PAPER_CN.md](PAPER_CN.md)）的落地规范：论文定义"量什么"，本规范定义"怎么量"。

## 1. 定位

HCLR（人类认知杠杆率）= 模型输出总和 / 使用者介入总和，用于衡量使用者的判断对AI输出的影响程度。采集协议是HCLR的**常驻测量层**：它不按需触发，而是在每一次对话中自动记录任务事件。

```text
HCLR = ΣO / ΣI
  O = 任务事件内模型输出Token（或字符）总和，含全部生成轮次
  I = 使用者介入Token（或字符）总和，不含初始任务描述
```

## 2. 核心概念

| 概念 | 定义 |
|---|---|
| 任务事件 | 一个有主题的对话单元：从使用者提出请求到成果产出（可含多轮交互） |
| O0 | 模型的初始生成（冻结保存，不可覆盖） |
| 介入 | 使用者针对模型输出的反馈/纠正/约束/方向调整（不计任务描述） |
| O1 | 介入后的最终成果 |
| C1 | 第一轮确认（adopt / partial / reject）——成果是否被采纳 |
| C2 | 第二轮确认（approved / rejected / pending）——成果是否获受众认可 |
| 状态 | S0未采用 / S1已采用待确认 / S2已采用未获认可 / S3已采用并获认可 |

## 3. 采集时机（钩子）

| 时机 | 动作 |
|---|---|
| 任务事件开始 | 识别有主题的请求，记录 `task_description`（不计入I），冻结O0 |
| 每次模型输出 | 累加O（输出字符/Token） |
| 每次使用者介入 | 记录介入文本，累加I |
| 任务事件结束 | 保存O1，标记任务事件边界 |
| 会话结束 | **请求C1**（一行确认：adopt / partial / reject） |
| 延迟回访 | 成果实际使用后**请求C2**（approved / rejected / pending） |

## 4. 记录字段

与 [schema/hclr-record.schema.json](schema/hclr-record.schema.json) 一一对应：

```text
task_id, domain, model, audience,
task_description（不计I）, O0, O1, O_total,
interventions[ {seq, text, kind, timestamp} ], I, I_metric,
C1, C1_note, C2, C2_note, status, created_at, period
```

## 5. 口径规则

1. **自动记录场景**默认以Token（或字符）计介入量；**人工记录场景**默认以判断数计。
2. **同一曲线内不得混用口径**（token/字符/判断数）。
3. I **不含**初始任务描述；O **含**全部生成轮次。
4. 测量边界：Token只测显性表达形式，不测认知成本与信息价值；使用者可通过压缩表达、合并命题、省略依据人为抬高比率——**采集时须保留原始记录以便复核**。
5. 单样本即可运行：`HCLR_j = O_j/I_j` 在第一个任务事件产生时即可计算；多样本用于趋势与稳定性。

## 6. 确认流程（双重确认）

```text
C1（第一轮，会话结束时）: adopt / partial / reject
  → 采纳进入S1，未采纳进入S0
C2（第二轮，成果实际使用后）: approved / rejected / pending
  → 认可进入S3，未认可进入S2，无反馈保持"待确认"
```

- C1由使用者本人确认；C2以真实受众反馈为准；
- 延迟结果回填原批次，不单独计为新任务事件；
- 缺失反馈记为"待确认"，不猜测。

## 7. 隐私与数据

- 原始记录（含完整对话）**本地保存**，不随公开仓库发布；
- 公开示例（如 [examples/PILOT_CASE_CN.md](examples/PILOT_CASE_CN.md)）为**匿名化**整理；
- 单条记录建议字段：O0/O1可保留匿名化文本，真实姓名、受众身份、完整反馈非必需。

## 8. 参考实现

| 组件 | 说明 |
|---|---|
| [pilot-data/pilot.py](pilot-data/pilot.py) | 命令行记录工具（new / record / c1 / c2 / report），git忽略，本地使用 |
| [schema/hclr-record.schema.json](schema/hclr-record.schema.json) | 记录数据格式（v0.2） |
| 自动化建议 | 在对话系统加消息钩子：assistant输出累加O、user介入累加I、会话结束自动请求C1 |

## 9. 平台适配

| 场景 | 采集方式 |
|---|---|
| Hermes（当前） | 对话内嵌采集：assistant在会话中记录O/I，会话结束请求C1 |
| 其他Agent框架 | 消息中间件/钩子：监听assistant/user消息，按字段记录 |
| 手动模式 | 任何工具可用：对话结束后按本规范人工填写记录 |

## 10. 与TOA询问法的配合

[TOA询问法](https://github.com/tri-chinaroot/toa-questioning) 解决"如何把意图问出来"，HCLR解决"如何量介入杠杆"。TOA记录（TOA-项目名-时间.md）本身就是一次任务事件，可直接作为HCLR采集对象：

```text
先用TOA逐题征询（问出意图） → 再用HCLR记录（量出杠杆）
```
