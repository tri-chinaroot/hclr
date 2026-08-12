# Human Cognitive Leverage Ratio: A Method for Assessing AI Users' Sparse Intervention Capability

## From a Few Critical Judgments to Adoptable AIGC Outputs

> **Document statement**: This is the original method manuscript of HCLR (v0.1), published for dissemination, citation, and community discussion. It is not a formal peer-reviewed journal publication. All formulas and reference values herein are **experimental designs**: P1–P5 is an ordinal scale that has not yet been calibrated, and the intervention amount I defaults to token counts (or character counts) in automated recording scenarios, measuring explicit intervention expression leverage rather than the cognitive investment required to form judgments. Readers should not interpret any numerical value as a validated measurement. For the latest and simplest description of the method, see the repository [README](README.md).
>
> Version: 0.1 (method manuscript, second-draft original)
>
> Author: tri-chinaroot

## Abstract

Generative AI can quickly produce long, dense content, but a user's critical contribution to the result does not necessarily take the form of an equally large edit. In practice, a very short intervention — such as "this data only shows correlation, not causation," "why assume competitors stay put," or "this strategy ignores execution capability" — can cause the AI to reorganize most of the content and turn an unusable draft into a result the user is willing to adopt and deliver to the intended audience. This paper calls this capability the **sparse intervention capability** of AI users and proposes the Human Cognitive Leverage Ratio (HCLR) as an adoptable assessment method.

HCLR does not assess general human intelligence, nor does it judge whether AIGC outputs reach some abstract objective truth. It addresses a more concrete practical question: within a given model, task domain, and relatively stable usage period, how much effective change does a user produce in AIGC outputs through how many explicit interventions? This paper adopts a **double confirmation** completed by the user: after the output is generated, the user confirms whether they adopt it; after the output reaches the target audience, the user confirms, based on real feedback, whether the audience recognizes it. The first confirmation forms an immediate reference value; the second forms an outcome-confirmed value. Records without sufficient audience feedback remain in a pending state and are not treated as failures.

This paper provides the definition of HCLR, its calculation, a five-level scope of change, intervention amount recording methods, and personal-level aggregation methods, along with a lightweight measurement protocol. After continuously completing both confirmations, a user can form a personal HCLR trend curve to observe whether they can produce more adoptable outputs with fewer, more critical judgments. The data can also supplement model providers' existing instant good/bad feedback: the first confirmation records whether the result was actually adopted, and the second records whether it gained audience recognition after adoption. If the original output, sparse interventions, and revised output are all preserved, recurring high-leverage interventions can be converted into model evaluation items and training material. This paper does not claim HCLR as the only indicator of AI usage ability, nor as a permanent ability score detached from model and task contexts.

**Keywords:** generative AI; human cognitive leverage ratio; sparse intervention; AI user; output adoption; audience recognition; assessment method

---

## 1. Problem Statement

Generative AI has lowered the cost of content production. Research reports, business analyses, product proposals, code documentation, and communication materials can all be drafted in a short time. As content becomes abundant, human work does not simply disappear; it shifts partly from directly producing large volumes of text toward judging which content is usable, which assumptions do not hold, which critical constraints are missing, and how to adjust the output so that it truly enters use and delivery.

This change creates an asymmetry worth measuring separately:

\[
10000\text{ generated content units}
\rightarrow
10\text{ critical judgments}
\rightarrow
1\text{ critical challenge}
\rightarrow
50\%-100\%\text{ of output restructured}
\]

These numbers illustrate a pattern, not fixed ratios. They describe a structure: AI generates densely, humans intervene sparsely, and AI then performs large-scale revision based on a few interventions. The human's explicit output is small, but that output may determine whether the result is adoptable.

Existing human-AI collaboration research commonly measures completion time, accuracy, preference, adoption rate, or combined human-AI performance. A human-AI combination is not necessarily superior to either alone, and explanatory interfaces do not guarantee complementary performance. [2][3]

Experiments on cognitive forcing further show that interface design affects whether people seriously examine AI suggestions. [6]

Algorithm aversion research shows that people may reduce their use of algorithms after seeing them err; allowing users to modify algorithm outputs may increase their willingness to continue using them. [4][5]

These studies show that "whether a human can intervene" affects usage behavior, but they do not directly answer another question: can the capability of different users to convert AIGC drafts into adoptable outputs through a few interventions be independently recorded and compared?

This paper proposes the Human Cognitive Leverage Ratio. Its goal is not to build a complete theory of human cognition or human-AI collaboration, but to offer a practically usable assessment method. It answers three questions:

1. What behavior counts as one sparse intervention?
2. How do we judge whether an intervention produced effective change?
3. How can continuous HCLR recording let us observe whether the same user's sparse intervention capability changes?

The basic claim is: in AIGC use, human value cannot be measured only by text volume, prompt length, or number of edits. The extent to which a few interventions effectively change the final output is another capability dimension worth observing.

## 2. Method Positioning and Applicability Boundaries

### 2.1 What HCLR Assesses

HCLR assesses:

> Within a given large language model, task domain, and observation period, the extent to which an AI user, through limited explicit interventions, causes AIGC outputs to be first adopted by the user and then, after the output reaches the audience, confirmed by the user as recognized based on feedback.

This definition involves four objects:

- **User**: the person who reads, judges, and intervenes in AIGC outputs;
- **Intervention**: a correction, challenge, constraint, supplement, or framework adjustment the user provides to the AI;
- **Output change**: the substantive difference in content, conclusions, structure, or direction of the AIGC output before and after intervention;
- **Practical effectiveness**: in the first round, the user confirms personal adoption; in the second round, the user confirms audience recognition based on feedback.

HCLR is primarily a performance indicator, not a stable personality trait. A person may show high leverage in strategic analysis tasks but not necessarily in legal writing or code review. Therefore, any score must be attached to the model, task domain, and observation period.

### 2.2 What HCLR Does Not Assess

HCLR does not directly assess:

- A person's full cognitive capability;
- Whether AIGC outputs have unquestionable objective correctness;
- The user's moral level or integrity;
- The overall capability of the large model itself;
- The long-term social value of the final output;
- An employee's overall performance;
- A unified ranking of all AI usage abilities.

Information value theory emphasizes that the value of information depends on whether it changes action and outcomes, not on the number of symbols. [1] HCLR is close to this practical orientation but does not require building a complete utility function for every task. For most knowledge work, whether the output is adopted by the user and fits the target audience is a more direct and more easily recorded judgment.

### 2.3 Why "Objective Correctness" Is Not Required

The claim that "adopted" and "recognized" do not equal objective correctness is itself valid, but it does not constitute a reason to reject HCLR. HCLR evaluates the adoptability of an output in a specific task, not the establishment of a universal truth standard.

Consulting recommendations, strategic plans, product definitions, brand expressions, and organizational decisions often have no single right answer. They require factual and logical foundations, but ultimately they are subject to context, goals, resources, risk preferences, and audience judgment. If "objective correctness" were a precondition for every task, assessment would slide into endless epistemological debate and lose practical value.

Therefore, HCLR adopts operational criteria:

1. After the output is generated, is the user willing to take responsibility for and actually adopt it?
2. After the output reaches the target audience, does the user confirm, based on real feedback, that the audience recognizes it?

After the first confirmation, an adoption HCLR can be formed. The second confirmation has a time lag; outputs not yet delivered or without feedback remain "pending" and are not counted as unrecognized. The entire judgment process is completed by the user; no researcher or system is required to collect data directly from the audience.

### 2.4 The Large Model as a Given Tool Environment

HCLR does not require completely separating model capability from outcomes. Within a relatively stable usage period, the large model can be treated as a given tool environment. The user judges the quality of the model's draft, the result after intervention, and whether to continue using the model. When the user changes or abandons a model, scores under the old model remain as historical records but no longer represent current usage capability.

Therefore, HCLR should be written as a conditional indicator:

\[
HCLR(u\mid m,d,T)
\]

where:

- \(u\) denotes the user;
- \(m\) denotes the model and its version;
- \(d\) denotes the task domain;
- \(T\) denotes the relatively stable observation period.

When comparing different users, the same or comparable model environment should be used. If models differ, scores should be reported separately, not treated as a context-free personal ability ranking.

### 2.5 It Is Only an Assessment Method

HCLR can be used alongside other indicators such as task completion time, fact-checking accuracy, user satisfaction, creativity, business outcomes, or expert review scores. It does not replace these indicators, nor does it claim to be the only method.

It fills a specific gap: when AI handles most content generation, evaluating people by text volume and edit count underestimates the value of a few critical judgments. HCLR attempts to make that value visible.

## 3. Core Concepts

### 3.1 Dense Generation

Dense generation means that AI produces large amounts of interrelated content at low marginal cost, including factual statements, analyses, assumptions, recommendations, code, diagram captions, or expressive text. "Dense" is not a strict mathematical concept; it is relative to the amount of human intervention: AI output is usually much longer than the critical judgments the human subsequently provides.

### 3.2 Sparse Intervention

A sparse intervention is an explicit input by the user that is small in number but capable of causing substantive change to the AIGC output. An intervention can be a sentence, a constraint, a counterexample, or a new problem framing.

Typical interventions include:

1. Fact correction: "This market size uses a different statistical caliber."
2. Reasoning challenge: "This data only shows correlation, not causation."
3. Assumption challenge: "Why assume competitors will not react?"
4. Constraint addition: "This strategy ignores the organization's execution capability."
5. Decision requirement: "Without P&L, no expansion conclusion can be drawn."
6. Framework replacement: "The current framework does not answer the question the sponsor actually wants solved."

"Sparsity" should be judged after the fact from the relationship between intervention amount and scope of change, not by limiting how many questions a user may ask. The user may read fully and intervene freely; if only a few judgments produce the main changes, a sparse intervention pattern is observable.

### 3.3 Autonomous Intervention

This paper records only substantive judgments formed and expressed by the user. AI may help present material, organize content, or execute edits, but AI-generated critiques cannot be re-counted as human cognitive contributions.

This does not require that interventions be completely free of AI assistance. In practice, users may form judgments through multiple conversational turns. Measurement should distinguish:

- AI raises a question and the user only confirms it;
- The user adds a new judgment on top of an AI suggestion;
- The user proactively raises a challenge the AI did not express.

The latter two categories can be recorded, but the source of the intervention should be noted. This annotation is for explaining scores and need not become a complex theoretical variable.

### 3.4 User Adoption

User adoption means that the output after intervention reaches the standard the user is willing to actually use or deliver. Adoption cannot be replaced by "looks better"; behavioral traces should be kept wherever possible, for example:

- Using that version as the official report;
- Submitting the recommendation to a decision-maker;
- Using the content for presentation, communication, or publication;
- Passing the code, proposal, or requirement into the next workflow;
- Explicitly choosing this version over the original.

Define the adoption variable:

\[
A_j=
\begin{cases}
1,& \text{the output after the }j\text{th intervention is adopted}\\
0,& \text{not adopted}
\end{cases}
\]

> Note: The adoption variable \(A_j\) in early drafts is the same in meaning as the first-round confirmation \(C_{1j}\) in Section 3.5. Formal records and calculations uniformly use \(C_{1j}\); \(A_j\) is no longer used separately.

Graded values from 0 to 1 can also be used to represent partial adoption, adoption after revision, and direct adoption. In the early stage of the method, however, binary recording more easily forms a consistent standard.

### 3.5 User Double Confirmation

HCLR's effectiveness judgment is completed by the user at two points in time; no system is required to contact the target audience directly.

The first confirmation occurs after output generation and intervention are complete. The user confirms whether they are willing to adopt or deliver the output:

\[
C_{1j}=
\begin{cases}
1,& \text{the user confirms adoption}\\
0,& \text{the user does not adopt}
\end{cases}
\]

The second confirmation occurs after the output reaches the target audience and generates feedback. Still completed by the user based on observed feedback, it confirms whether the audience recognizes the output:

\[
C_{2j}\in\{1,0,\varnothing\}
\]

Here, 1 means the user confirms audience recognition, 0 means the user confirms audience non-recognition, and \(\varnothing\) means not yet delivered or insufficient feedback. Pending is not failure and must not be counted as 0.

The target audience may be clients, supervisors, partner teams, users, reviewers, or the public. "Recognition" does not require the audience to agree with everything; it means the output meets the threshold for entering the next action, communication, or decision. The user's ability to understand audience concerns and make AIGC outputs meet that standard is itself part of AI application capability.

To keep recording simple, the second confirmation only needs the status and the category of feedback basis, such as explicit acceptance, entering the next stage, core acceptance with requested local revisions, core rejection, or still pending. The system need not store audience identity or full original feedback.

### 3.6 Scope of Effective Change

HCLR needs to record how much of the output the intervention changed, and whether the change touched important parts of the task. This paper adopts a five-level scale:

| Level | Scope of change | Judgment example |
|---|---|---|
| P1 | Local change | Fixing one fact, wording, or single item without affecting main conclusions |
| P2 | Module change | Changing one major paragraph, functional module, or a complete argument |
| P3 | Conclusion change | Changing a core conclusion, or jointly revising multiple major parts |
| P4 | Plan change | Changing main recommendations, plan ordering, delivery structure, or action direction |
| P5 | Framework change | Changing the problem definition, analytical framework, or the organization of the whole output |

Define the scope of change of the \(j\)th intervention as:

\[
P_j\in\{1,2,3,4,5\}
\]

Scope of change is not equal to the number of rewritten characters. Deleting one erroneous core assumption may change an entire conclusion; rewriting hundreds of words of wording may still be P1. Scoring should be based on the role of the final output in the task, not on the size of the textual difference.

### 3.7 Intervention Amount

Intervention amount represents the explicit input the user provides to change the output. This paper recommends recording the following separately rather than hastily combining them into a complex cost:

- Number of independent judgments;
- Number of independent semantic propositions;
- Number of intervention characters or tokens;
- Number of intervention turns;
- Review and expression time.

**Automated default metric**: In automated recording scenarios, the intervention amount I defaults to the token count (or character count) of the intervention text. Rationale: objective, automatically measurable, reproducible, and zero annotation burden for the user. Boundary: token count measures expression length; it does not include the reviewing, searching, fact-checking, and reasoning costs required to form judgments, nor does it equal the number of independent judgments. Therefore, token-based HCLR reflects "explicit intervention expression leverage," not complete cognitive investment. Because different models use different tokenizers, the tokenizer metric must be declared when comparing across models.

Among the metrics above, the number of independent semantic propositions is closest to "information amount." For example, "the data caliber is inconsistent, so market sizes cannot be compared directly" contains a factual judgment and an inferential judgment, and can be counted as two related propositions. In research scenarios requiring a semantic metric, judgment counts or semantic proposition counts can still be used; the two metric families must be declared in records and must not be mixed.

## 4. Computing HCLR

### 4.1 First Round: Adoption HCLR

> **Experimental formula**: P1–P5 is an ordinal scale and should not be used as an interval value in calculations before calibration; the metric for I_j (judgments / characters / turns) must be declared when recording. For formal use, follow the metric specifications in the repository README.

The first confirmation measures how much adoptable output change the user produces per unit of intervention. For the \(j\)th intervention:

\[
\boxed{
HCLR^{(1)}_j=
\frac{C_{1j}\cdot P_j}{I_j}
}
\]

where \(C_{1j}\) is whether the user adopts, \(P_j\) is the scope of change, and \(I_j\) is the intervention information amount. If the user does not adopt, the first confirmation fails and that intervention produces no adoption leverage.

### 4.2 Second Round: Recognition HCLR

> **Experimental formula**: The second round is computed only on records with audience feedback; pending (S1) is not counted as 0. Denominator metric is the same as 4.1.

After the output reaches the audience, the user completes the second confirmation based on actual feedback:

\[
\boxed{
HCLR^{(2)}_j=
\frac{C_{1j}\cdot C_{2j}\cdot P_j}{I_j}
}
\]

The second confirmation applies only to records that have received audience feedback. If the user confirms audience recognition, \(C_{2j}=1\); if non-recognition is confirmed, \(C_{2j}=0\). Both confirmations are completed by the user; the difference is that the first is based on the user's own adoption decision, and the second is based on feedback after the output enters a real audience scenario.

### 4.3 Pending State

The second confirmation usually occurs later than the first. Each record should retain the following states:

| State | First round | Second round | Meaning |
|---|---:|---:|---|
| S0 not adopted | 0 | not entered | Output did not meet the user's adoption standard |
| S1 adopted, pending | 1 | \(\varnothing\) | Adopted, but insufficient audience feedback yet |
| S2 adopted, not recognized | 1 | 0 | User confirms audience non-recognition |
| S3 adopted and recognized | 1 | 1 | Both confirmations passed |

S1 must not be merged with S2; otherwise, outputs not yet delivered or with long feedback cycles would be wrongly counted as failures. Second-round feedback should be backfilled to the task batch of the original output, not to a new task batch created when feedback is received.

### 4.4 Information Leverage and Time Leverage

> **Metric note**: In automated recording scenarios, I_semantic defaults to intervention token counts (or character counts); in manual recording scenarios, independent judgment counts or semantic proposition counts can be used. The two metric families must not be mixed within the same curve.

Intervention information amount and intervention time answer different questions; they should not be forced into a single denominator. Both the first and second rounds can compute information leverage and time leverage separately.

First-round information leverage:

\[
HCLR^{(1)}_{I,j}=
\frac{C_{1j}\cdot P_j}{I_{semantic,j}}
\]

Second-round information leverage:

\[
HCLR^{(2)}_{I,j}=
\frac{C_{1j}\cdot C_{2j}\cdot P_j}{I_{semantic,j}}
\]

Time leverage replaces the denominator with intervention time \(T_j\). Information leverage answers "how much adoptable output change does one unit of explicit judgment produce," while time leverage answers "how much adoptable change is produced per unit of time."

### 4.5 Personal-Level Aggregation

For user \(u\) with \(n\) interventions within the same model, similar tasks, and observation period, the first-round cumulative HCLR is:

\[
\boxed{
HCLR^{(1)}(u\mid m,d,T)=
\frac{\sum_{j=1}^{n}C_{1j}\cdot P_j}
{\sum_{j=1}^{n}I_j}
}
\]

The second-round cumulative HCLR is computed only on the set \(J_2\) of records that have completed the second confirmation:

\[
\boxed{
HCLR^{(2)}(u\mid m,d,T)=
\frac{\sum_{j\in J_2}C_{1j}\cdot C_{2j}\cdot P_j}
{\sum_{j\in J_2}I_j}
}
\]

Computing a simple arithmetic mean of single-intervention HCLR values is not recommended, because very short interventions can produce extreme values. Dividing cumulative effective change by cumulative intervention amount is more stable. When reporting second-round HCLR, the number of second-round-confirmed samples and the pending ratio must also be reported.

### 4.6 Personal Trend Curve

The primary use of HCLR is within-user longitudinal self-assessment, not cross-person absolute ranking. Compute by week, month, quarter, or fixed task batch:

\[
HCLR^{(1)}_1,HCLR^{(1)}_2,\ldots,HCLR^{(1)}_T
\]

\[
HCLR^{(2)}_1,HCLR^{(2)}_2,\ldots,HCLR^{(2)}_T
\]

The two curves respectively represent changes in the user's efficiency in converting AIGC outputs into "outputs I am willing to adopt" and "outputs confirmed as recognized through audience feedback." A second-round confirmation rate can also be reported:

\[
VCR_t=
\frac{\sum_{j\in J_{2,t}}C_{1j}C_{2j}}
{\sum_{j\in J_{2,t}}C_{1j}}
\]

A rising curve can serve as a reference for improvement in sparse intervention capability, but it cannot be interpreted independently of context. Model version, task domain, task difficulty, target audience, and intervention amount unit should remain relatively stable. If these conditions change, a new observation interval should begin or the curve should be clearly marked.

An HCLR trend curve does not prove that a person's general cognitive level has improved. It reflects whether, in a specific AIGC usage environment, the user is increasingly able to produce more adoptable outputs with fewer, more critical interventions.

### 4.7 A Simplified Example

> **Unit statement**: This example uses the "task event" as the unit — three judgments jointly produce one P4 change, and one reference value is computed over the total intervention amount. Individual interventions should not double-count the same output change; applications must fix the unit (see README metric specifications).

A user reviews an AI-generated market entry report and makes three independent judgments:

1. "The sample only covers first-tier cities and cannot represent national demand."
2. "Competitors will not keep prices unchanged."
3. "Channel construction costs are missing; the current profit forecast cannot support the entry conclusion."

The three judgments are counted together as 3 intervention semantic propositions. Based on them, the AI changes the main recommendation from "enter the whole country immediately" to "pilot in two regions first and add channel-cost verification." The user adopts the new version, and the scope of change is rated P4.

The first-round confirmation value is:

\[
HCLR_I^{(1)}=\frac{1\times4}{3}=1.33
\]

If, after the output is submitted to the investment committee, the user confirms from the meeting result that the plan enters the pilot stage, the second-round state is S3 and a corresponding \(HCLR_I^{(2)}\) is formed. If the meeting has not yet occurred, the state is S1, not S2. This value has no intrinsic cross-domain meaning; it is meaningful only when compared under the same scoring rules, similar tasks, and the same model environment.

## 5. Lightweight Measurement Protocol

### 5.1 Minimum Record Unit

A complete record contains at least:

1. Task description and target audience;
2. Model, version, and main generation parameters;
3. Original AI output;
4. The user's original intervention content;
5. AI output after intervention;
6. First confirmation: whether the user adopts;
7. Second-round status: recognized, not recognized, or pending;
8. The category of feedback basis for the second confirmation;
9. Scope of change P1 to P5;
10. Intervention information amount and time used.

These records are sufficient to compute basic HCLR; no complex reasoning graph, full causal graph, or economic utility model is required first.

### 5.2 Basic Measurement Process

1. Clarify the AI user, task goal, and target audience.
2. Save the original AIGC version before intervention.
3. Save the user's interventions verbatim, without post-hoc polishing.
4. Save the AI output generated from the intervention.
5. The user completes the first confirmation: whether to adopt.
6. The user records scope of change, intervention amount, and time.
7. Adopted outputs enter the S1 "pending" state.
8. After the output reaches the audience and feedback is generated, the user completes the second confirmation.
9. Second-round results are backfilled to the original task batch.
10. Form a personal HCLR trend curve on a fixed schedule.

The entire process only requires the user to complete brief confirmations at two points in time. The system does not need to send questionnaires to the audience or obtain audience identity or full feedback content.

### 5.3 The User as the Primary Rater

HCLR is a self-assessment method. The user is both the intervener and the primary recorder of the two confirmations and the scope of change. This design is not meant to produce a context-free objective score, but to let the user continuously observe their own AI application performance at low cost.

To reduce arbitrariness, the system can provide uniform definitions and examples, requiring the user to complete P1 to P5 ratings before knowing the current HCLR result. In research or organizational applications, a small sample may be re-rated by a second rater, but independent rating is not a necessary step for every record.

### 5.4 Basis for the Second Confirmation

The user can complete the second confirmation based on the following feedback:

- The client accepts the deliverable;
- A decision meeting allows the plan to enter the next stage;
- A supervisor adopts the recommendations in the report;
- Users complete the intended action;
- Review passes or core content is accepted;
- The audience requests local revisions but accepts the core output;
- The audience explicitly rejects or overturns the core output.

Different tasks' recognition forms cannot be directly mixed into a single standard. At the start of a task, the user should clarify "what counts as recognition" and keep it consistent within similar tasks. Recording only the feedback basis category and second-round status greatly reduces information acquisition difficulty.

### 5.5 Conditions for Longitudinal Comparison

HCLR is prioritized for within-user longitudinal comparison. When interpreting a trend curve, at least record:

- Model and version;
- Task domain and difficulty;
- Target audience type;
- P1 to P5 scoring rules;
- Intervention amount unit;
- Proportion with completed second confirmation;
- Observation period.

If the model, task, or evaluation standard changes significantly, a new observation interval should begin or the environment change should be marked on the curve. Different users can exchange cases and methods, but HCLR should not be used for absolute ranking when conditions differ greatly.

## 6. Method Validation

As an adoptable self-assessment method, HCLR must prove that it is easy to record, easy to understand, and provides information that traditional output metrics do not. The validation focus is not to prove the formulas are universal truths, but to test whether users can use the method over time to observe their own changes.

### 6.1 Content Validity

Invite users with practical AIGC experience to review the following definitions:

- What counts as one independent intervention;
- What first-round adoption is;
- Under what circumstances the second confirmation can be completed;
- Whether P1 to P5 covers common changes;
- Whether intervention information amount is easy to record;
- Whether the two confirmations add unacceptable workload.

Collect real cases through interviews and check whether common interventions are missing from the categories. Revise the scale where necessary instead of insisting on a priori conceptual completeness.

### 6.2 Scoring Repeatability

Ask users to rate the same set of anonymized cases with P1 to P5 at different times, and check whether their judgments are roughly stable. In research settings, a second rater can review a small sample to identify confusing boundaries in the scale. If P3 and P4 are persistently hard to distinguish, the definitions and examples should be revised.

### 6.3 Second-Round Confirmation Rate

The practical difficulty of the second confirmation is not evaluation theory; it is that users may leave the system after copying or delivering outputs and fail to backfill results. Therefore, key observations include:

- First-round confirmation rate;
- Number of tasks entering S1;
- Second-round completion rate;
- Average time from first to second confirmation;
- Ratio of S2 to S3;
- Whether the second-round completion rate improves after reminders.

If the second-round completion rate is too low, recognition HCLR will suffer obvious selection bias. The system should display "pending" separately and must not let confirmed samples represent all outputs.

### 6.4 Explanatory Power of the Trend Curve

Observe the same person over multiple periods in the same model and similar tasks. If the HCLR curve is consistent with the user's own reviews, effective intervention cases, and changes in the second-round confirmation rate, the method has practical explanatory power.

Scores are not required to be permanently stable. Model upgrades, task changes, professional growth, or audience changes will alter the curve. The method's job is to record these changes and their contextual conditions, not to interpret HCLR as a fixed personality trait.

### 6.5 Incremental Value

Compare the HCLR curve with simple indicators:

- Prompt length;
- Number of revised characters;
- Number of interventions;
- Completion time;
- Instant user satisfaction;
- Number of final outputs.

If HCLR can identify capability changes of "little output but large change" that traditional output metrics cannot, it provides incremental value. HCLR does not need to replace other indicators; it only needs to reveal different information.

## 7. Suggested Initial Research Design

### 7.1 Research Purpose

The initial study only needs to test four questions:

1. Can the two confirmations be completed at low cost in real AIGC tasks?
2. Can users use the P1 to P5 scale consistently?
3. Can the HCLR trend curve reflect changes in the user's sparse intervention performance?
4. Can delayed reminders and personal curve feedback improve the second-round confirmation rate?

### 7.2 Task Selection

Choose tasks that participants are familiar with, have clear target audiences, and can produce actual deliverables, for example:

- Market research summaries;
- Business strategy recommendations;
- Product requirement documents;
- Membership operation plans;
- Project review reports;
- Technical proposal reviews.

Tasks need not have a single correct answer, but it must be clear who uses the output, who it is delivered to, and what counts as adoption and recognition.

### 7.3 Participants and Environment

Let AI users record continuously over multiple periods with a relatively stable model version and similar tasks. Participants may read, ask, and intervene freely; there is no limit on the number of interventions. After the study, observe whether high-value changes concentrate in a few interventions.

The initial study focuses on within-user longitudinal change; it does not require placing all participants in identical tasks for ranking. Researchers should record model, task, and audience conditions to explain curve changes.

### 7.4 Data Collection

For each task, save:

- Initial generation result;
- Each substantive human intervention;
- Final adopted version;
- First confirmation;
- Second confirmation status and time;
- Second-round feedback basis category;
- Scope of change rating;
- Intervention amount and time.

To reduce privacy risk, study data can retain only anonymized text, intervention types, and confirmation states. Real client names, audience identities, and full feedback are not necessary data for HCLR.

### 7.5 Analysis Methods

The initial study is primarily descriptive:

- First-round HCLR per period;
- Second-round HCLR per period;
- Second-round confirmation rate;
- Pending ratio;
- Share of high-leverage interventions in all effective change;
- P1 to P5 distribution;
- Relationship of HCLR to revised characters, prompt length, and time;
- Curve differences before and after model or task changes.

Because ratios can have extreme values, report medians, quantiles, and cumulative values as well as means.

### 7.6 Adoptability Judgment

Whether the method holds up first depends on whether it meets these conditions:

- Users find the cost of the two confirmations acceptable;
- Users can understand the meaning of scores and curves;
- P1 to P5 can be used consistently;
- The curve can explain real high-leverage intervention cases;
- Scores are not misread as general intelligence or absolute performance;
- Compared with text volume and edit count, it provides new self-understanding;
- Personal curve feedback increases willingness to keep recording.

This is consistent with the paper's positioning: HCLR itself must also be a method that practitioners can continuously adopt.

## 8. Applications to Improving Large Model Generation Quality

### 8.1 From Instant Preference to Real Usage Outcomes

Large model products typically allow users to give instant good/bad ratings on conversation results. Such signals express immediate preference but cannot show whether the user actually adopted the output, nor whether the output gained audience recognition in a real scenario.

Human feedback has been used to improve models' adherence to user intent, for example through supervised fine-tuning and reinforcement learning with demonstrations and output rankings. [7] HCLR's double confirmation is not another simple good/bad button; it is delayed feedback closer to actual usage outcomes: the first confirmation records whether the output was actually adopted, and the second records whether it was recognized by the audience after adoption.

### 8.2 The Complete Feedback Chain

For model providers, one high-value record should contain:

\[
O_0\rightarrow h\rightarrow O_1\rightarrow C_1\rightarrow C_2
\]

where:

- \(O_0\): the model's original output;
- \(h\): the user's sparse intervention;
- \(O_1\): the output after intervention;
- \(C_1\): the user's adoption confirmation;
- \(C_2\): the user's second confirmation based on audience feedback.

Recording only the final output would wrongly attribute the human's critical judgments to the model. Preserving the original output and the intervention difference makes it possible to identify where the model needs a few human corrections, and which corrections repeatedly move results from unusable to usable.

### 8.3 Quality Indicators Model Providers Can Obtain

HCLR still evaluates the user. Model providers should not treat HCLR directly as a model score, but can compute from the same data:

- Direct adoption rate without intervention;
- Adoption rate after intervention;
- Double-confirmation pass rate;
- Human intervention amount needed to reach the first confirmation;
- Human intervention amount needed to reach the second confirmation;
- Distribution of S1, S2, and S3 states;
- Distribution of frequent high-leverage intervention types.

If, after a model upgrade, users achieve more S3 outcomes with fewer interventions, that is closer to real generation value improvement than an instant like rate.

### 8.4 From High-Leverage Interventions to Training and Evaluation Material

Recurring high-leverage interventions can expose systematic model weaknesses. For example, if many users only need to point out "competitors will not stay put" to move strategic reports from first-round rejection to double-confirmation pass, dynamic competition assumptions may be a stable blind spot of the model.

Providers can convert such interventions into:

- Regression evaluation items;
- Pre-generation self-check items;
- Training examples;
- Personalized model preferences;
- Quality diagnosis labels for specific domains.

The value of HCLR data lies not only in the score, but in the traceable relationship of "original output — human intervention — output change — double confirmation."

### 8.5 Improving the Second-Round Feedback Rate

Users often leave the system after copying, downloading, or delivering outputs, so the second confirmation cannot rely only on users returning voluntarily. Products can ask for the first confirmation when the user marks "ready to use," downloads a file, or creates a share link, and send one low-disturbance reminder at an appropriate time:

> Did the previously adopted output gain recognition from its target audience?

Second-round options can stay short: recognized; core recognized with local revisions; not recognized; not yet delivered; still pending. Behavioral signals can only trigger the question; they cannot automatically equal adoption or recognition.

After users complete double confirmation, the system returns their personal HCLR curve, high-value intervention types, and second-round confirmation rate. Users provide outcome feedback and receive self-improvement information in return; this is more likely to sustain behavior than simply asking users to help the provider improve the model.

### 8.6 Privacy and Attribution Boundaries

Double confirmation does not require uploading client identity, meeting records, or full audience feedback. The system can store only confirmation states, feedback basis categories, intervention types, and necessary anonymized differences.

Model providers must also distinguish model contribution from human contribution. An excellent post-intervention output does not directly prove that the original model output was high quality; on the contrary, the human intervention amount required to reach double confirmation is itself an important quality signal.

## 9. Potential Misuse and Limitations

### 9.1 Treating Scope of Change as Scope of Destruction

If users pursue only high P values, they may deliberately propose disruptive opinions that cause large rewrites. HCLR constrains this through the two confirmations. Changes that never enter actual adoption cannot form first-round scores, and outputs without audience recognition cannot form second-round value.

### 9.2 The User Bears All Confirmation

The user both intervenes, rates, and completes both confirmations, which may lead to overestimating their own contribution. This limitation comes from the method's choice of low cost and sustainability. HCLR explicitly calls its results "self-reference assessment values," not independent certification results.

Optional sample re-rating, version records, and feedback basis categories can reduce arbitrariness, but every record should not be turned back into a complex external review.

### 9.3 Second-Round Missingness Is Not Random

Users are more likely to backfill feedback for successful, important, or memorable outputs; failed and ordinary outputs may remain in S1 for a long time. When reporting second-round HCLR, the pending ratio must be disclosed; do not display only S3 cases.

### 9.4 Persuasion May Come from Non-Content Factors

Audience recognition may be affected by identity, power, expression style, or organizational relationships. HCLR does not interpret recognition as objective correctness; it treats it as evidence of usability in a specific social context. If the research goal requires excluding identity effects, anonymous evaluation can be added; if the goal is to evaluate real-world usage performance, these contextual factors need not all be excluded.

### 9.5 Model Changes

Model upgrades can change draft quality and responsiveness to interventions. Therefore, curves must be accompanied by model version and observation period. Cross-model comparisons should re-establish baselines; historical scores cannot be carried over directly.

### 9.6 Task Differences

The scopes of change in strategic plans, marketing copy, and code review are not directly interchangeable. HCLR is suitable for use within the same domain and task family. Cross-domain aggregation can only serve as a personal profile description, not precise ranking.

### 9.7 Metric Gaming

If HCLR is directly tied to performance, compensation, or termination decisions, users may split interventions, exaggerate scope of change, or select tasks that produce high scores. In its early stage, HCLR is more suitable for:

- Self-review;
- AI usage training;
- Comparing different working methods;
- Identifying high-value intervention cases;
- Observing personal growth curves.

Until reliability, validity, and gaming resistance are fully validated, HCLR is not recommended for high-stakes personnel decisions.

### 9.8 Fewer Interventions Is Not Always Better

Sparsity is a possible outcome of high-leverage intervention, not a requirement to reduce feedback. Complex tasks may need multiple rounds of intervention. HCLR rewards effective change per unit of intervention; it does not deny the value of careful review.

## 10. Discussion

AIGC has made large-scale content generation easy, and has also weakened the explanatory power of traditional output metrics. How many words a person wrote or how many prompts they sent may not reflect their true contribution. The value of some users appears as their ability to identify a few decisive problems and use very short expressions to push AI through large-scale restructuring.

This capability includes professional judgment as well as understanding of the task, application context, and target audience. When a user finds that "missing P&L cannot support the expansion conclusion," that reflects constraint judgment; when the user expresses the output in a way the investment committee can accept, that reflects information application ability. Together they determine whether AIGC output moves from generated material to a usable deliverable.

Double confirmation turns this capability into low-cost continuous recording. The first round answers "do I actually adopt it," and the second answers "after the output reaches a real audience, is it recognized." Both rounds are confirmed by the user, keeping data collection simple; the time series turns a single high-leverage case into an observable personal trend curve.

HCLR does not need to prove that post-intervention outputs are correct in every sense. It only requires clearly stating who the user is, who the target audience is, what behavior counts as adoption, what feedback counts as recognition, what scope the change occurred in, and how much explicit intervention the user made. Its rigor comes from clear boundaries and auditable records, not from reducing all tasks to a single truth or a single utility function.

For users, the HCLR curve provides a reference for whether sparse intervention capability is improving. For model providers, the same data chain can supplement instant preference feedback, helping identify the gap between original output and actual adoption, the gap between adoption and audience recognition, and recurring human high-leverage interventions. But the two uses must not be conflated: HCLR evaluates human intervention performance; model quality requires separately computing direct adoption rate, double-confirmation rate, and the human intervention amount needed to reach confirmation.

This paper therefore positions HCLR as a limited but useful method. It does not replace factual accuracy, business outcomes, expert evaluation, or user satisfaction, nor does it interpret a rising curve as general intelligence improvement. It answers a narrower question: in a relatively stable AIGC environment, is the user increasingly able, with fewer critical judgments, to make more generated content become outputs they are willing to adopt and that are confirmed by audience feedback.

## 11. Conclusion

This paper proposes the Human Cognitive Leverage Ratio for assessing the sparse intervention capability of AI users. Its basic process is:

\[
AI\text{ dense generation}
\rightarrow
human\text{ few critical interventions}
\rightarrow
AI\text{ restructures output}
\rightarrow
user\text{ first confirmation of adoption}
\rightarrow
output\text{ reaches audience}
\rightarrow
user\text{ second confirmation of recognition}
\]

The first-round cumulative HCLR is:

\[
\boxed{
HCLR^{(1)}(u\mid m,d,T)=
\frac{\sum_{j=1}^{n}C_{1j}\cdot P_j}
{\sum_{j=1}^{n}I_j}
}
\]

The second-round cumulative HCLR is computed on records with audience feedback:

\[
\boxed{
HCLR^{(2)}(u\mid m,d,T)=
\frac{\sum_{j\in J_2}C_{1j}\cdot C_{2j}\cdot P_j}
{\sum_{j\in J_2}I_j}
}
\]

By continuously recording the two values on a fixed schedule, users can form a personal trend curve and observe whether they can produce more adoptable outputs with fewer, more critical interventions. The curve is a reference for sparse intervention capability in AIGC usage contexts, not a measure of general cognitive level or a permanent ability score.

The same double-confirmation data may also help model providers improve generation quality. Compared with instant good/bad ratings, it further records whether the output was actually adopted and whether it gained audience recognition after adoption. If the original output, sparse interventions, and revised output are all preserved, frequent high-leverage interventions can be converted into model evaluation items and training material.

HCLR is not an objective truth standard, not a complete theory of human-AI collaboration, and not the only method for evaluating AI users. It is a low-cost, sustainable self-assessment method grounded in actual usage outcomes. Its value lies in making visible a capability that is often overlooked: after AI takes over dense generation, humans can still determine, through extremely few but critical judgments, whether the output is truly usable.

## Sources

[1] https://doi.org/10.1109/TSSC.1966.300074 — Howard (1966), Information Value Theory
[2] https://arxiv.org/abs/2006.14779 — Bansal et al. (2021), Does the Whole Exceed its Parts?
[3] https://doi.org/10.1145/3290605.3300233 — Amershi et al. (2019), Guidelines for Human-AI Interaction
[4] https://doi.org/10.1037/xge0000033 — Dietvorst et al. (2015), Algorithm Aversion
[5] https://doi.org/10.1287/mnsc.2016.2643 — Dietvorst et al. (2018), Overcoming Algorithm Aversion
[6] https://arxiv.org/abs/2102.09692 — Buçinca et al. (2021), To Trust or to Think
[7] https://arxiv.org/abs/2203.02155 — Ouyang et al. (2022), Training language models to follow instructions with human feedback
