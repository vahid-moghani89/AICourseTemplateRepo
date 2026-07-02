# A3 Specification — Template

> Fill every section **before** your first agent interaction. Your git history / file timestamps should make that credible.

## Objective

One paragraph: what analysis, on what data, to answer what question.

## Inputs

- `data/synthetic_survey/survey.csv` (1,200 rows — see `data/README.md` for documented quirks)
- `data/sample_200.csv` (fixed classification sample)
- `data/codebook_concerns.md` (5-category coding scheme)

## Outputs (exact filenames — AC3 checks these)

| File | Contents |
|---|---|
| `outputs/exclusion_ledger.md` | Per-rule exclusion counts; raw N → final N |
| `outputs/table1.csv` | Per education group: N, mean/SD of trust & adopt scores |
| `outputs/comparison.md` | Inferential test, assumption checks, result |
| `outputs/text_classification.csv` | sample_200 with assigned category per row |
| `outputs/text_distribution.md` | Category distribution + 10 examples |

## Cleaning rules

Write each rule so a stranger could apply it identically. Cover at least: duplicates, reverse-coded items, impossible values, label harmonization — and what happens to rows affected (exclude vs. repair, and why). Add rules for anything else you find.

## Acceptance criteria (≥6, each binary-checkable)

- `AC1:` Final N is stated and equals 1,200 minus exclusions, with a per-rule exclusion count.
- `AC2:` Reverse-coded items are re-coded; evidenced by item-total correlations all positive.
- `AC3:` Every output file listed above exists and is reproduced by rerunning.
- `AC4:` [yours]
- `AC5:` [yours]
- `AC6:` [yours]

*A criterion is binary-checkable if two people would always agree whether it passed. "Data is properly cleaned" — no. "No resp_id appears twice in the cleaned data" — yes.*
