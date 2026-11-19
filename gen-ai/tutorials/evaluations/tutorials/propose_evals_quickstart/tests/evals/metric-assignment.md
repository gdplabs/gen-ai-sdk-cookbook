# Metric assignment: Banking Assistant Chatbot

The maintained source for what this eval checks and for which cases. Read it before classifying new cases or
changing a metric. The values (case ids and suites in `banking_assistant_chatbot_assignment.py`, metric configs in `evaluators.py`) live
in code; this file holds the definitions and the reasons. Keep both in step.

## Qualities

| id | quality | source | metric |
|---|---|---|---|
| R1 | The answer covers every key fact of `expected_response` | user (dataset gives expected answers) | `GEvalCompletenessMetric` (threshold 1.0) |
| R2 | The answer is supported by the supplied policy context, nothing added | derived: `chatbot/prompts/generation.system.txt` "Selalu berdasarkan jawaban pada konteks yang diberikan. Jangan menambahkan informasi atau asumsi yang tidak ada." | `GEvalGroundednessMetric` (threshold 1.0, `additional_info` says what the context is) |
| R3 | The answer is in Indonesian, the language of the question | user ("answers in Indonesian"); derived: `generation.system.txt` "Selalu merespons dalam Bahasa Indonesia." | `GEvalLanguageConsistencyMetric` (threshold 0.5) |
| R4 | The chatbot refuses exactly when the expected response is a refusal | derived: `chatbot/banking_assistant_chatbot.py` FAILURE_RESPONSE and the guardrail / relevance stages; dataset rows labeled "Tidak bisa Jawab" | `GEvalRefusalAlignmentMetric` (threshold 0.5) |

## Suites

| suite | definition | boundary examples (dataset ids) | reference | qualities |
|---|---|---|---|---|
| answerable | A bank-policy question whose answer is in the supplied context; `expected_response` is the factual answer | fact-check question that the context corrects → answerable (6); list question → answerable (7) | `expected_response`: it is *the* answer, extracted from the context | R1, R2, R3 |
| refusal | A question the chatbot must not answer: another bank / general knowledge, prompt injection or unusual output format, a customer's private data; `expected_response` is "Tidak bisa Jawab" | another bank's general info → refusal (54); prompt injection asking for HTML → refusal (58); personal bill question → refusal (70) | `expected_response`, read only for its refusal status (the wording differs from the chatbot's fixed refusal) | R4 |

## Not evaluated

- R1/R2/R3 in the refusal suite: the refusal is a fixed Indonesian string; groundedness's rubric scores any refusal as ungrounded, and completeness against "Tidak bisa Jawab" duplicates R4.
- R4 in the answerable suite: a wrongful refusal already fails R1 (no key facts) and R2.
- Exact match against `FAILURE_RESPONSE`: the generation stage may also refuse in other words; and checking the constant would re-implement the target's own logic.
- The chatbot's intermediate fields (`predicted_is_guardrails`, `predicted_is_relevant`, `response` chain of thought): the dataset has no labels for them; the final answer is the outcome.

## Calibration

- none yet.

## Gotchas

- Both suites are small (7 and 3 cases): one case moves a suite's accuracy by 14 or 33 points.
- `expected_response` for refusal rows is "Tidak bisa Jawab", not the chatbot's "Maaf, saya tidak bisa menjawab pertanyaan tersebut."; R4 compares refusal status, not wording.
- Row 1's expected answer keeps the context's footnote marker ("White****/Grey").

## Classifying new rows

1. Match each row against the definitions and boundary examples above, never against earlier assignments.
2. One suite fits: add `"<id>": "<suite>"` to `CASE_SUITE`.
3. None fits, or two fit: ask the user. A new kind of case gets a new row in Suites first.
4. Report the outcome: `clean`, `changed` (needs approval), or `blocked`.

## Changing the assignment

| Change | Edit |
|---|---|
| Add or reclassify a row | `CASE_SUITE` |
| New suite | a Suites row here + `build_evaluators` |
| Rename or merge suites | `CASE_SUITE` values + `build_evaluators` + the Suites row |
| Add or drop a quality in a suite | `build_evaluators` + the Suites row |
| Change a metric or its threshold | `build_evaluators`, in every suite that uses it + the Qualities row |
| A variant for one suite | a new Qualities row here + `build_evaluators` |
