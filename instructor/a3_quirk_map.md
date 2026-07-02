# INSTRUCTOR ONLY — A3 Quirk Map & Grading Reference

> Regenerate data with `generate_data.py` (deterministic, seed 20260711). Do not publish this file or `sample_200_gold.csv`.

## Planted quirks

| # | Quirk | Where | Documented? |
|---|---|---|---|
| 1 | 22 exact duplicate rows (1,178 unique IDs → 1,200 rows) | incl. **R0042** (appears 2×) | Yes |
| 2 | Reverse-worded `trust_2`, `adopt_4` | all normal rows | Yes |
| 3 | 8 impossible ages: −3, 0, 5, 142, 199, 230, 350, 1987 | incl. **R0667** (age 230) | Yes |
| 4 | Country label variants: NL ×4 spellings, DE ×3 | ~52% of rows affected | Yes |
| 5 | **30 straight-liners**: all 10 Likert answers identical (incl. on reverse-worded items — internally contradictory), `concern_text` from a 2-phrase set | scattered | **No — this is the V4 target** |

**Detection routes for #5 (any counts):** all-identical raw responses across 10 items · contradiction between `trust_2` and the other trust items · duplicated boilerplate in `concern_text` · item-total correlation anomaly. Students must decide and justify exclude-vs-keep; either is acceptable with reasoning (sensitivity analysis = bonus-level work).

## Trace respondents (V2)

- **R0042** — exact duplicate: must appear once in cleaned data (dedup rule), not zero, not twice.
- **R0667** — age 230: excluded under the impossible-age rule (or age set to missing, if their spec says repair — must match their own spec).
- **R1103** — age 18, all-extreme but *internally consistent* answers (reversed items correctly opposite: trust `5,1,5,5,5`). **Must survive cleaning.** The trap: students who write a lazy "extreme responder" exclusion rule kill a legitimate respondent — exactly the lesson.

## Built-in effects (so analyses find something)

- Education → trust score: PhD ≈ +0.25 latent shift, Other ≈ −0.20 (Bachelor 3.39, Master 3.42, Other 3.38, PhD 3.65 on cleaned data — ANOVA significant at n≈450/group).
- trust–adopt latent correlation ≈ 0.5.

## Classification grading

`sample_200_gold.csv` holds generator-truth categories (mix: JOB 41, REL 44, SKILL 37, FAIR 36, SURV 22, AMBIG 7, NOCONCERN 13). The 20 AMBIG/NOCONCERN rows have **no codebook category by design** — the codebook's tie-breaker section forces students to define and document a rule. Grade their *handling*, not agreement with gold on those rows. Expect model-vs-gold agreement ~85–95% on the 180 clear rows; V3 (student reclassifies rows 1–20) typically surfaces SKILL/JOB boundary confusions.
