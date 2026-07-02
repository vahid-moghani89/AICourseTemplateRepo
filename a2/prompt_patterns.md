# Assignment 2 — Prompt Patterns A, B, C

> Use these patterns as given, filling the bracketed slots. You may tighten them, but every pass must keep its **constraints block** — the constraints are what make the output auditable.

---

## Pattern A — The Mirror (reverse outline)

```
You are analyzing the argument structure of an academic text. Do NOT improve,
edit, or comment on quality.

Task: extract the text's argument as a numbered list of claims, in the order
they appear. For each claim: state it in one sentence, using the author's own
key terms where possible, and note which sentence(s) it comes from.

Constraints:
- Extraction only. No suggestions, no praise, no criticism.
- If a passage asserts nothing (pure description or transition), list it as
  "[no claim: description/transition]".
- If two claims contradict or one is unsupported by what precedes it, flag it
  with "[tension]" or "[unsupported]" — but do not resolve it.

Text:
[PASTE my_text.md]
```

**How to read the output:** every claim the model extracted that you didn't intend, and every claim you intended that it missed, is a finding about your *text*, not about the model.

---

## Pattern B — Constrained line edit

```
Edit the following academic text for clarity and concision.

Hard constraints:
1. Preserve the meaning of every claim. Do not strengthen hedged claims or
   hedge strong ones.
2. Add no new claims, no new citations, no new examples.
3. Keep the author's voice; do not normalize to generic academic prose.
4. Target audience: [VENUE/AUDIENCE from your Step 0].
5. After the edited text, output a complete change table:
   | # | Original | Revised | Reason |
   Every change must appear in the table — including small ones.

Text:
[PASTE the text as corrected after Pass A]
```

**Your audit duty:** diff the edited text against the original yourself. The model's change table is routinely incomplete and occasionally misrepresents what it changed — finding those gaps is part of the assignment.

---

## Pattern C — The Hostile Reviewer

```
You are Reviewer 2: expert in [YOUR FIELD], constructive but unsparing.
Review the text below against exactly these five criteria:

1. Contribution clarity — is it stated, specific, and plausible?
2. Logic — does each step follow from the previous one?
3. Evidence–claim fit — does any claim outrun what is shown or cited?
4. Counterarguments — what is the strongest objection the author ignores?
5. Precision — vague terms, undefined constructs, weasel words.

Output: your THREE strongest objections, ranked. For each: the criterion it
falls under, the exact sentence(s) at issue (quote them), and why it matters.
Do not pad with minor style points. Do not soften.

Text:
[PASTE your revised text]
```

**Then argue back.** For each objection you must rule: *valid — will address* (say how) / *valid — out of scope here* (say why) / *invalid* (rebut in two sentences). Accepting all three uncritically is the same failure as rejecting all three reflexively.
