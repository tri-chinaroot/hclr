# HCLR Collection Protocol Specification (v1.0)

> Version: 1.0.0 (2026-08-12) ｜ Author: tri-chinaroot ｜ 中文版: [PROTOCOL_CN.md](PROTOCOL_CN.md)
>
> This document defines **how to continuously collect HCLR data in any AI conversation system**. It is the operational companion to the method manuscript ([PAPER_EN.md](PAPER_EN.md)): the paper defines *what to measure*; this protocol defines *how to measure it*.

## 1. Positioning

HCLR (Human Cognitive Leverage Ratio) = total model output / total user intervention, measuring how much the user's judgments shape AI output. The collection protocol is HCLR's **resident measurement layer**: it is not triggered on demand — it records task events automatically in every conversation.

```text
HCLR = ΣO / ΣI
  O = total model output tokens (or chars) in a task event, including all generation rounds
  I = total user intervention tokens (or chars), excluding the initial task description
```

## 2. Core Concepts

| Concept | Definition |
|---|---|
| Task event | A topical conversation unit: from the user's request to the produced output (may span multiple rounds) |
| O0 | The model's initial generation (frozen, never overwritten) |
| Intervention | User feedback/correction/constraint/direction aimed at model output (excluding the task description) |
| O1 | The final output after interventions |
| C1 | First confirmation (adopt / partial / reject) — whether the output was adopted |
| C2 | Second confirmation (approved / rejected / pending) — whether the audience recognized the output |
| State | S0 not adopted / S1 adopted pending / S2 adopted but not recognized / S3 adopted and recognized |

## 3. Collection Triggers (Hooks)

| Moment | Action |
|---|---|
| Task event starts | Identify a topical request; record `task_description` (excluded from I); freeze O0 |
| Each model output | Accumulate O (output chars/tokens) |
| Each user intervention | Record the intervention text; accumulate I |
| Task event ends | Save O1; mark the event boundary |
| Session ends | **Request C1** (one-line confirmation: adopt / partial / reject) |
| Delayed follow-up | **Request C2** after the output is actually used (approved / rejected / pending) |

## 4. Record Fields

One-to-one with [schema/hclr-record.schema.json](schema/hclr-record.schema.json):

```text
task_id, domain, model, audience,
task_description (excluded from I), O0, O1, O_total,
interventions[ {seq, text, kind, timestamp} ], I, I_metric,
C1, C1_note, C2, C2_note, status, created_at, period
```

## 5. Measurement Rules

1. **Automated recording** defaults to tokens (or chars) for the intervention amount; **manual recording** defaults to number of judgments.
2. **Never mix metrics within the same curve** (tokens / chars / judgments).
3. I **excludes** the initial task description; O **includes** all generation rounds.
4. Measurement boundary: tokens measure explicit expression form only — not cognitive cost or information value; users can inflate the ratio by compressing expression, merging propositions, or omitting rationale — **keep raw records for audit**.
5. A single sample is sufficient to run: `HCLR_j = O_j/I_j` is computable from the first task event; more samples serve trends and stability.

## 6. Confirmation Flow (Double Confirmation)

```text
C1 (first round, at session end): adopt / partial / reject
  → adopted enters S1; not adopted enters S0
C2 (second round, after actual use): approved / rejected / pending
  → recognized enters S3; not recognized enters S2; no feedback stays "pending"
```

- C1 is confirmed by the user; C2 is based on real audience feedback;
- Delayed results are backfilled to the original batch, not counted as new task events;
- Missing feedback is recorded as "pending" — never guessed.

## 7. Privacy & Data

- Raw records (including full conversations) are **stored locally**, not published with the public repository;
- Public examples (e.g. [examples/PILOT_CASE_EN.md](examples/PILOT_CASE_EN.md)) are **anonymized**;
- Per-record guidance: O0/O1 may keep anonymized text; real names, audience identities, and full feedback are not required fields.

## 8. Reference Implementation

| Component | Note |
|---|---|
| [pilot-data/pilot.py](pilot-data/pilot.py) | CLI recording tool (new / record / c1 / c2 / report); git-ignored, local use |
| [schema/hclr-record.schema.json](schema/hclr-record.schema.json) | Record data format (v0.2) |
| Automation suggestion | Add message hooks to the conversation system: assistant outputs accumulate O, user interventions accumulate I, auto-request C1 at session end |

## 9. Platform Adaptation

| Scenario | Collection method |
|---|---|
| Hermes (current) | In-conversation collection: the assistant records O/I during the session and requests C1 at the end |
| Other agent frameworks | Message middleware/hooks: listen to assistant/user messages and record per fields |
| Manual mode | Works with any tool: fill in a record by hand after the conversation per this protocol |
