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
| I (intervention amount) | Character count of intervention messages (auto-counted, chars metric) |
| P (scope of change) | P1–P5, suggested by the assistant and confirmed by the user |
| C1 (first confirmation) | At conversation close: adopt / partial / reject |
| C2 (second confirmation) | After real-world use: approved / rejected / pending |

## Process

1. At the close of each topical conversation, the assistant requests C1 (one-line reply);
2. P is suggested by the assistant and confirmed by the user;
3. A summary report is generated every 10 tasks or weekly;
4. Raw records stay local (not published in the repository, to protect privacy).

## Sample Data (First 2 Tasks)

| Task | Domain | P | I (chars) | C1 | State | Example intervention |
|---|---|---|---|---|---|---|
| pilot-001 | Empirical design | P4 plan | 28 | partial | S1 | "OK, but I hope every conversation can be auto-counted without extra operations" |
| pilot-002 | Conceptual clarification | P3 conclusion | 60 | adopt | S1 | "Correction: you are not the model being used; the bound large model is …" |

## Current Snapshot

```text
Tasks: 2
Post-intervention adoption rate: 100% (2/2)
P distribution: P3×1, P4×1
Average intervention: 44 chars/task
Output leverage (AI output / intervention): 3.9
Second confirmation: none yet (outputs not yet used in practice)
```

## Significance

- **Zero-burden validation**: the user only answers one line of C1 at conversation close; P confirmation is one phrase;
- **Real data**: P, I, and C1 are real conversation records, not simulated data;
- **Direct paper backfill**: as data accumulates, Sections 6–7 of the manuscript move from "validation plan" to "initial validation results";
- **Counterfactual control**: same model (DeepSeek v4 flash) and unified metric (chars) satisfy the conditions for longitudinal comparison.

Raw records are kept locally under `pilot-data/` (consistent with the LICENSE: full user conversation records are not published).
