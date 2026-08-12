# HCLR CLI 原型使用说明

零依赖（Python 标准库），数据保存在本地 SQLite `~/.hclr/hclr.db`，默认不联网。

## 安装

```bash
cd app
chmod +x hclr.py
# 可选：加入 PATH
ln -s "$(pwd)/hclr.py" /usr/local/bin/hclr
```

## 使用流程

```bash
# 1. 初始化
python3 hclr.py init

# 2. 创建任务事件
python3 hclr.py task add \
  --title "会员体系分析报告" \
  --domain 咨询 \
  --model deepseek-v4 \
  --audience 部门领导

# 3. 冻结 AI 初稿 O0（不可覆盖）
python3 hclr.py draft freeze <task_id> --file draft.txt
# 或 python3 hclr.py draft freeze <task_id> --text "初稿内容"
# 或 cat draft.txt | python3 hclr.py draft freeze <task_id>

# 4. 记录人类介入（可多次）
python3 hclr.py intervene <task_id> "补充约束：需按ABC集团现状裁剪" --kind constraint
python3 hclr.py intervene <task_id> "结论需要区分短期与长期建议" --kind conclusion_revision
# 介入量默认按判断数计（每条=1）；可用 --metric chars 或 turns 切换口径

# 5. 设置改变范围 P1-P5
python3 hclr.py p <task_id> 4 --note "整体方案结构改变"

# 6. 第一轮确认
python3 hclr.py confirm1 <task_id> adopt --p 4
# 或 python3 hclr.py confirm1 <task_id> reject

# 7. （成果触达受众后）第二轮确认
python3 hclr.py confirm2 <task_id> approved --note "领导采纳并进入下一阶段"
# 或 confirm2 <task_id> rejected / pending（待确认，默认）

# 8. 生成报告 / 导出
python3 hclr.py report
python3 hclr.py report <task_id>
python3 hclr.py export --output hclr.json
```

## 设计说明

- 计算单位是**任务事件**，单条介入只作为事件内部追踪记录；
- O0 冻结后不可覆盖，防止事后改写历史；
- P 只按顺序等级记录，报告不输出合成总分（见 SCORING.md）；
- 第二轮 `pending` 记为待确认（S1），不计 0；
- 报告同时显示 P 分布、第二轮完成率与已确认认可率，两者分母不同。

## 后续版本计划

- 自动版本差异比较（O0 vs O1）；
- 介入类型自动分类；
- 分周期（月度）趋势；
- 无介入任务的直接采用率统计；
- 导出 CSV；
- 排行榜模式（统一任务集，需另行设计）。
