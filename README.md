# HCLR — 人类认知杠杆率

> **Human Cognitive Leverage Ratio**
> 评估 AI 使用者对模型输出的影响程度 —— 一种面向 AI 使用者的自我评估方法。

AI 写了很多，但哪些关键变化真正来自你？

HCLR 帮助你记录从 AI 初稿到最终成果的全过程，观察你的**稀疏认知介入**（少量但关键的人类判断）对模型输出产生了多大影响，并持续跟踪你的个人变化趋势。

## 为什么需要 HCLR

在与大模型协作时，同样一段输出，不同使用者的处理方式完全不同：

- 有的人照单全收，不做任何修改；
- 有的人逐句润色，改动很多但方向未变；
- 有的人只提出三五条关键判断，却让成果发生方向性改变。

HCLR 关注的不是“谁写得快”，而是：

> **在使用者的指导下，AI 产出发生了多大范围、多少价值的改变；使用者是否愿意采纳成果；成果进入真实场景后是否获得受众认可。**

## 核心概念

| 概念 | 含义 |
|---|---|
| 原始生成 `O0` | 模型在无介入条件下产出的初始输出 |
| 人类介入 `h` | 使用者主动、自主发出的关键判断（纠正、约束、方向调整等） |
| 介入后成果 `O1` | 经过介入后产出的最终成果 |
| 第一轮确认 `C1` | 使用者确认介入后的成果是否达到自己愿意采纳的标准 |
| 第二轮确认 `C2` | 成果触达受众后，使用者根据真实反馈确认成果是否获得认可 |

完整过程链：

```text
O0 → h → O1 → C1 → C2
```

## 项目结构

```text
hclr/
├── README.md              # 本文件
├── METHOD.md              # HCLR 方法说明（白皮书）
├── SCORING.md             # 计分规则与指标定义
├── LIMITATIONS.md         # 局限性与边界条件
├── PRIVACY.md             # 隐私与数据政策
├── PRODUCT_VISION.md      # 产品愿景与商业化路径
├── examples/              # 分领域示例
├── schema/                # 记录数据 Schema
├── app/                   # 记录与计算工具
└── docs/                  # 其他文档
```

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/tri-chinaroot/hclr.git
cd hclr

# 使用记录工具（CLI）
python3 app/hclr.py init
python3 app/hclr.py task add "撰写会员体系分析报告" --domain 咨询
python3 app/hclr.py draft freeze <task_id>   # 冻结 AI 初稿 O0
python3 app/hclr.py intervene <task_id> "补充约束：需按ABC集团现状裁剪" --kind constraint
python3 app/hclr.py confirm1 <task_id> adopt  # 第一轮确认
python3 app/hclr.py confirm2 <task_id> approved  # 第二轮确认
python3 app/hclr.py report <task_id>        # 生成报告
```

详见 [`app/README.md`](app/README.md)。

## 文档

- [方法说明 METHOD.md](METHOD.md) — 什么是 HCLR、如何记录
- [计分规则 SCORING.md](SCORING.md) — 指标、公式、口径
- [局限性 LIMITATIONS.md](LIMITATIONS.md) — 必须知道的边界
- [隐私政策 PRIVACY.md](PRIVACY.md) — 数据归属与安全
- [产品愿景 PRODUCT_VISION.md](PRODUCT_VISION.md) — 自我评估 → 厂商应用 → 排行榜

## 状态

- 当前版本：0.1（方法草案 + CLI 原型）
- 定位：**自我评估方法**，不是学术量表，不用于招聘、淘汰或跨人绝对排名
- 仓库当前为私有，稳定后可按作者决定公开

## License

见 [LICENSE](LICENSE)。（待作者确定开源协议）
