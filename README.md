# How Much Did Your Judgment Change AI?

> **The Human Cognitive Leverage Ratio (HCLR): A Method for AI Users to Assess Their Influence on Model Outputs**

**中文版 / Chinese version: [README_CN.md](README_CN.md)**

---

## Abstract

AI can generate a lot of content, but generating a lot is not the same as doing good work. Given the same AI output, different users handle it very differently: some accept it as-is, some polish it sentence by sentence, and some make just a few critical judgments that change the direction of the result.

HCLR (Human Cognitive Leverage Ratio) is a self-assessment method for AI users. It records the process from the initial AI draft to the final deliverable and observes how much the user's **sparse cognitive interventions** (few but critical human judgments) influenced the model output. Through **double confirmation**, it tracks whether the result was actually adopted and whether it gained audience recognition.

---

## 1. Why HCLR

Most existing tools only record whether users are satisfied (thumbs up/down). They cannot answer:

- Did the user actually change the AI output?
- At what level did the change occur — wording, content, conclusions, the whole plan, or the problem framing?
- How many key judgments did the user need to make the result acceptable?
- Over time, is the user getting better at producing larger effective changes with fewer interventions?

HCLR provides a lightweight, sustainable way to record and observe these questions.

## 2. Core Definitions

**HCLR is a self-assessment method for the sparse intervention capability of AI users.** Within a given AIGC model, task domain, and observation period, the user records the changes their limited explicit interventions made to the generated output, and performs two rounds of confirmation.

Conditional representation:

```
HCLR(u | m, d, T)
```

- `u`: user
- `m`: model and version (a relatively stable tool environment)
- `d`: task domain
- `T`: observation period

**The model is treated as a given tool environment.** HCLR does not require fully separating human and model contributions, but changing models, task domains, or audiences should be marked as a series breakpoint.

### Process Chain

```
O0 → h → O1 → C1 → C2
```

| Symbol | Meaning |
|---|---|
| `O0` | Original AI output (initial output without intervention) |
| `h` | Human intervention (active, autonomous critical judgment) |
| `O1` | Output after intervention (final deliverable) |
| `C1` | First confirmation: whether the user adopts the result |
| `C2` | Second confirmation: whether the audience recognizes the result, based on real feedback |

## 3. How to Record

### 3.1 Basic Unit: Task Event

The basic unit is a **task event**: one AI collaboration task from original generation through human interventions to a confirmable final output. Individual interventions are tracked within the event but are not scored separately, avoiding double-counting the same change.

### 3.2 Record Fields

- `task_id`, `domain`, `model` (model and version), `audience` (audience type)
- `O0` (original output, frozen and immutable), `O1` (final output)
- `interventions[]` (list: text, type, timestamp)
- `I` (intervention amount), `P` (scope of change P1–P5)
- `C1` (0/1), `C2` (1/0/pending), `C2_note` (basis for confirmation)
- Timestamps (created / confirmed / second confirmation)

Full field definitions: [`schema/hclr-record.schema.json`](schema/hclr-record.schema.json)

### 3.3 Human Intervention

An intervention is a **critical judgment actively and autonomously initiated by the user**, for example: fact correction, goal or scope adjustment, constraint addition, conclusion revision, analytical framework change, style and audience adaptation.

Two principles:

1. **Interventions must be initiated by the human.** AI must not decide (e.g., via active learning) when or what the human should review, or restrict review boundaries.
2. **Sparsity is an observed property after the fact**, not a pre-allocated feedback budget.

### 3.4 Intervention Amount (I)

Three metrics are supported; declare which one is used:

| Metric | Definition | Note |
|---|---|---|
| Tokens / chars | Token or character count of intervention text | **Default in automated recording** (objective, zero annotation burden) |
| Judgments | Number of independent semantic judgments / key opinions | Default in manual recording |
| Turns | Number of intervention turns | Simplest |

> **Important boundary**: explicit intervention amount is not equal to total cognitive investment (reviewing, searching, fact-checking, reasoning costs are not counted). HCLR measures "explicit intervention leverage," not a complete cognitive ability score.

### 3.5 Scope of Change (P1–P5)

| Level | Meaning | Example |
|---|---|---|
| P1 | Local wording, fact, or single-item change | Fixing a typo, adding a data point |
| P2 | One module, major paragraph, or one argument changed | Rewriting one argument |
| P3 | Multiple major contents or core conclusions changed | Adjusting the conclusion direction |
| P4 | Overall plan, main recommendation, or delivery structure changed | Restructuring the deliverable |
| P5 | Problem definition, analytical framework, or final direction changed | Redefining the problem |

> **Important**: P1–P5 is an ordinal scale, not a validated interval scale. Before calibration, P should be reported as a categorical variable and should not directly enter ratio calculations.

### 3.6 Double Confirmation

**First confirmation C1** (generation stage): whether the user adopts the result — `1` adopted / `0` not adopted.

**Second confirmation C2** (after the result reaches the audience): whether the audience recognizes it, based on real feedback — `1` recognized / `0` not recognized / `∅` pending.

- C2 is the user's interpretation of **real feedback**, not a prediction made at generation time, and does not require researchers to survey the audience directly;
- **Pending is not failure**: tasks without sufficient feedback are recorded as pending and must not be counted as 0; delayed feedback is backfilled to the **original task batch**;
- Reports should disclose the pending ratio.

**Result states:**

| State | C1 | C2 | Meaning |
|---|---|---|---|
| S0 | 0 | — | Not adopted |
| S1 | 1 | ∅ | Adopted, pending confirmation |
| S2 | 1 | 0 | Adopted, not recognized |
| S3 | 1 | 1 | Adopted and recognized |

## 4. Scoring & Reporting

### 4.1 Companion Metrics

| Metric | Definition | Note |
|---|---|---|
| Direct adoption rate | Adopted without intervention / all tasks | Baseline: initial output quality |
| Post-intervention adoption rate | C1=1 / tasks with intervention | Whether intervention yields adoptable results |
| Second-round completion rate | With C2 / C1=1 tasks | Feedback backfill completeness |
| Confirmed recognition rate | C2=1 / tasks with C2 | Recognition rate within confirmed samples |
| Average intervention amount | ΣI / number of tasks | Intervention cost per task |
| High-leverage cases | C1=1, C2=1, P≥P3, I≤median | Few interventions, high-value change |

> Distinguish **second-round completion rate** from **confirmed recognition rate** — they have different denominators; mixing them is a common mistake.

### 4.2 Reference Score (Experimental)

Before P calibration, the following mapping is only for **directional personal longitudinal observation**, not for cross-person comparison:

```
Task event reference = P tier / I
P1/P2→1, P3→2, P4→3, P5→4
```

This mapping is heuristic, not a psychometric conclusion. Reports must always show the raw P distribution alongside.

### 4.3 Periods & Missing Data

- Default observation period: calendar month (configurable);
- Mark breakpoints when model / domain / audience changes;
- With fewer than 10 tasks, show raw records only, no trend conclusions;
- Pending is not 0; provide optimistic (all pending as recognized) and conservative (all pending as not recognized) bounds;
- When the pending ratio exceeds 30%, second-round metrics should be marked "unreliable."

### 4.4 Leaderboard Conditions (Community Scenarios Only)

Cross-person comparison is **only allowed under strict conditions**: unified model and version; unified task set and initial outputs; unified intervention metric; change scope blind-rated by third parties or the community; auditable full interaction records; no selective recording (failed tasks must be included); review of anomalous results.

## 5. Important Boundaries

- HCLR is a **self-assessment reference**, not an objective truth standard;
- Not a general intelligence or overall cognitive level scale;
- Not the only way to evaluate AI usage ability;
- Primarily for **within-user longitudinal self-comparison**, not for absolute cross-person ranking;
- Not suitable as a high-stakes tool for hiring, dismissal, or performance ranking;
- A rising curve can only serve as a **reference** for changes in sparse intervention capability, not proof of cognitive improvement; a falling curve may result from harder tasks, model changes, or audience changes.

### Known Limitations

1. **P1–P5 not calibrated**: ordinal scale, not interval;
2. **Denominator does not measure cognitive investment**: intervention amount only captures explicit form;
3. **Common method bias**: all ratings come from the same user; C2 is the user's interpretation of feedback;
4. **Selection bias**: successful/important tasks are more likely to receive second-round backfill;
5. **Incomplete attribution**: the O0→O1 change is not necessarily entirely caused by human intervention (model stochasticity);
6. **Gaming risk**: users may inflate scores by choosing tasks, compressing expressions, or selectively recording.

## 6. Privacy & Data

- Records may contain business secrets, personal information, and client data;
- **Local-first**: records are stored locally by default and uploaded to no server;
- Data belongs to the user; it can be deleted or exported at any time;
- Any aggregation, anonymization, or third-party use (e.g., model provider optimization) requires a separate agreement covering purpose, duration, revocability, and contribution attribution;
- Model providers should distinguish: instant "good/bad" buttons ≠ first-round adoption confirmation ≠ second-round audience outcome confirmation; outstanding post-intervention results must not be fully attributed to the model.

## 7. Applications

| Level | Scenario | Note |
|---|---|---|
| Individual | Self-observation and review | Primary use case |
| Organization | Team collaboration comparison | Requires unified model/task conditions; not for performance judgment |
| Model provider | High-leverage intervention discovery | Repeated human interventions reveal model blind spots, evaluation items, and training material (second-layer application) |
| Community | Leaderboard / challenge | Strict condition control required, see 4.4 |

## Original Manuscript

The full method manuscript (with formulas, measurement protocol, and validation agenda):

- [Original method manuscript (EN)](PAPER_EN.md)
- [Original method manuscript (CN)](PAPER_CN.md)
- [Source ledger](PAPER-sources.json)

> The manuscript is labeled as a v0.1 method draft for dissemination, not a formal peer-reviewed publication. See the document statement at the top of each paper for details.

## 8. License

This repository (including documents and code) is under a **custom license**:

- **Non-commercial use is free**, provided that you (1) **open a GitHub Issue in this repository** to notify the author before use, and (2) **credit the author** in any derivative work;
- **Commercial use** requires a separate agreement with the author;
- Applies to all content in this repository (README, schema, code, etc.).

See [LICENSE](LICENSE) for details.

---

## Author

[tri-chinaroot](https://github.com/tri-chinaroot)

## Version

0.1 (method draft). Future versions will calibrate fields and scoring rules based on real usage feedback.
