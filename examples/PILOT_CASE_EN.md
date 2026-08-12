# HCLR Empirical Case: Conversation-Embedded Pilot

> Version: 2026-08-12 ｜ Model environment: DeepSeek v4 flash

## Background

After publishing the HCLR method manuscript, a **conversation-embedded collection** design was adopted to obtain real empirical data: AI assistant conversations are used directly as the source of task events. The user needs no extra form filling; statistics are fully automated.

## Design

| Element | Definition |
|---|---|
| Task event | One topical conversation (from request to confirmed output) |
| Model environment m | The bound large model (here: DeepSeek v4 flash); the AI assistant is the execution/presentation layer and does not enter the m parameter |
| O0 | Assistant's first-round output |
| h | User's intervention message |
| O1 | Output after intervention |
| O (numerator) | Total model output tokens (or chars) in the task event, including all generation rounds |
| I (denominator) | Total user intervention tokens (or chars), **excluding the initial task description** |
| HCLR | O / I (output/intervention leverage ratio) |
| C1 (first confirmation) | Result state: adopt / partial / reject |
| C2 (second confirmation) | Result state: approved / rejected / pending |

## Process

1. At the close of each topical conversation, the assistant requests C1 (one-line reply);
2. P is suggested by the assistant and confirmed by the user;
3. A summary report is generated every 10 tasks or weekly;
4. Raw records stay local (not published in the repository, to protect privacy).

## Sample Data (5 Tasks)

| Task | Domain | O | I | HCLR (O/I) | C1 | State | Example intervention |
|---|---|---|---|---|---|---|---|
| pilot-001 | Empirical design | 209 | 28 | 7.46 | partial | S1 | "OK, but I hope every conversation can be auto-counted without extra operations" |
| pilot-002 | Conceptual clarification | 134 | 60 | 2.23 | adopt | S1 | "Correction: you are not the model being used; the bound large model is …" |
| pilot-003 | HCLR revision & finalization | 8650 | 214 | 40.42 | adopt | S1 | "There are no auxiliary indicators anymore; P1–P5 as integers is fundamentally wrong." |
| pilot-004 | TOA release & promotion | 6424 | 385 | 16.69 | adopt | S1 | "Keep the same details. Also, my goal is that users can freely use this Skills…" |
| pilot-005 | Method form analysis | 2858 | 88 | 32.48 | adopt | S1 | "Are Skills usually single-shot? But HCLR needs statistics on every conversation…" |

## Current Snapshot

```text
Tasks: 5
HCLR = ΣO / ΣI = 18275 / 775 = 23.58
Numerator O (model output chars total): 18275 | avg per task: 3655
Denominator I (intervention chars total, excluding task description): 775 | avg per task: 155
Result states:
  Post-intervention adoption rate: 5/5 = 100%
  Second confirmation: none yet (outputs not yet used in practice)
```

> Note: O/I for pilot-003/004/005 are computed from real message statistics in the Hermes session database (O = assistant text chars total; I = user intervention chars total, excluding the initial task description); C1 pending user confirmation.

## Significance

- **Zero-burden validation**: the user only answers one line of C1 at conversation close; P confirmation is one phrase;
- **Real data**: O, I, and C1 are real conversation records, not simulated data;
- **Direct paper backfill**: as data accumulates, Sections 6–7 of the manuscript move from "validation plan" to "initial validation results";
- **Counterfactual control**: same model (DeepSeek v4 flash) and unified metric (chars) satisfy the conditions for longitudinal comparison.

Raw records are kept locally under `pilot-data/` (consistent with the LICENSE: full user conversation records are not published).
