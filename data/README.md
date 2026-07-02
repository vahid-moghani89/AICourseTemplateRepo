# `synthetic_survey/survey.csv` — Data Documentation

**Fully synthetic** survey on attitudes toward AI at work. 1,200 rows. Safe to send to any AI service.

## Fields

| Field | Description |
|---|---|
| `resp_id` | Respondent ID (`R0001`–) |
| `age` | Years |
| `gender` | Female / Male / Non-binary / Prefer not to say |
| `country` | Country of residence |
| `education` | Bachelor / Master / PhD / Other |
| `trust_1`–`trust_5` | "I trust AI systems at work" scale, 1–5. **`trust_2` is reverse-worded** ("I would double-check anything an AI system tells me") |
| `adopt_1`–`adopt_5` | Adoption-intention scale, 1–5. **`adopt_4` is reverse-worded** |
| `concern_text` | Open answer: "What concerns you most about AI at your work?" |

## Documented quirks (handle them; your cleaning rules say how)

1. **Duplicate respondents** — some rows appear more than once (exact copies).
2. **Reverse-worded items** — `trust_2` and `adopt_4` must be re-coded before scale scores.
3. **Impossible ages** — a handful of values no living respondent can have.
4. **Inconsistent country labels** — the same country appears under several spellings.

> This list is **not guaranteed to be complete.** Real datasets never come with a complete quirk list either. (See A3, check V4.)

## Companion files

- `sample_200.csv` — fixed 200-row sample for the classification task (same rows for everyone; do not re-sample).
- `codebook_concerns.md` — the 5-category coding scheme for `concern_text`.
