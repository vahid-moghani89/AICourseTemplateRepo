# Session 6 — Specify, delegate, verify: in miniature (hands-on, 25 min)

This is the A3 workflow at one-tenth scale. Same rhythm, tiny task.

## 1. Write a five-line spec (5 min — before touching the agent)

Your agent will produce `table1.md` from `data/synthetic_survey/survey.csv`: **N and mean trust score per education group.** Write the spec in a new file `my_s6_spec.md`. Skeleton:

```
Task: produce table1.md — N and mean trust score per education group,
from data/synthetic_survey/survey.csv.
Handle the documented data quirks (see data/README.md) before computing.
AC1: <your acceptance criterion — checkable with a plain yes/no>
AC2: <your second criterion — a different kind of check than AC1>
Plan first: restate your plan and wait for my approval before running anything.
```

Writing the two ACs is the exercise. The test: *could a stranger check it yes/no without asking what you meant?* ("The table is correct" fails the test. "Group Ns sum to the post-cleaning N, which is stated" passes.)

## 2. Plan first (3 min)

Give the agent your spec. It restates its plan — **read the restatement**. Anything misread? Correct it *now*, before anything runs, and note what you corrected.

## 3. Let it run, then verify both criteria yourself (10 min)

- One criterion by **making the agent show and explain its code** ("explain line 12" is a legitimate move).
- The other by an **independent recomputation** — e.g., ask a *fresh* chat (or a spreadsheet, or a one-line pandas call you request separately) for the mean trust of one education group, and compare.

## 4. Log it (2 min)

`ai_use_log.md`: spec written first? plan corrected? both ACs verified, how? That four-line entry is A3's rubric in miniature — you've now done every graded move once.
