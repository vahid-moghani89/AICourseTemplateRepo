# Session 5 — Your first delegation (hands-on, 25 min)

**Before you start:** `bash check_agent.sh` shows green (agent logged in). Red? Raise a hand in the chat *now* — the fallback procedure takes two minutes.

## The task — give this to your agent, verbatim

Copy-paste exactly this (panel or terminal, your choice):

```
Explore this repository. Then examine data/synthetic_survey/ and write
summary.md: what the dataset contains, and any data-quality problems you find.
```

## While it runs — your actual job

1. **Read its narration.** Don't just wait for the result — the loop (plan → tool → observe → decide) is the lesson.
2. **Note one moment where it decided something you didn't specify.** (Where to save the file? Which tool to use? What counts as a "problem"?) Write that moment down — one sentence. We collect a few in the debrief.

## When it finishes — verify like it's Session 6 already

Open its `summary.md` **next to** `data/README.md` and answer three questions:

- **Found:** which of the four documented quirks did it catch?
- **Missed:** which did it miss? (Silence about a documented quirk is a finding about the *agent*, not the data.)
- **Over-claimed:** is anything in `summary.md` *claimed but not checked* — stated as fact without code or counts behind it?

Log the session in your `ai_use_log.md` (one entry: task, tool, one thing you verified, one thing you'd do differently).

*The one-sentence note from step 2 is tomorrow's lesson arriving early: an agent fills every gap in your instructions with a decision of its own. Session 6 is about making those decisions yours.*
