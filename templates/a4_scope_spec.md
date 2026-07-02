# A4 Scope Spec — Template (one page, hard limit)

> Bring a draft to the Session 8 clinic. Approval of this page is the gate for A4. One page forces the scoping decisions that protect your 15 hours.

## 1. Option & lane

Option [1/2/3/4a/4b] · Lane [A: code-first / B: agent-directed]

## 2. What I will build (3 sentences max)

The artifact, the data it runs on (name the public/synthetic source — link if external), and who in research would use it for what.

## 3. Done means (the contract)

| # | Checkable statement |
|---|---|
| D1 | e.g., "Pipeline classifies all 800 reviews into the 6 categories with no manual step" |
| D2 | e.g., "Cohen's κ vs. my 100 gold labels is computed and reported (whatever its value)" |
| D3 | … |

*Note D2's phrasing: "is computed and reported", not "is above 0.7". You commit to honest measurement, not to results.*

## 4. Validation plan (from the brief — name each prescribed component and how you'll do it)

E.g., Option 1: gold labels (100 items, committed before pipeline results) · accuracy + κ · 5-disagreement error table · robustness probe (paraphrased codebook, 50 items).

## 5. What I am explicitly NOT doing

≥3 bullets. The most important section — this is where "mini" lives.

## 6. Risk & fallback

The one thing most likely to fail, and the smaller version you'll cut to if it does (this is what your midpoint email will reference).

## 7. Hours budget

| Phase | h |
|---|---|
| Setup & data | |
| Build | |
| Validation | |
| Documentation & demo | |
| **Total (≤15)** | |
