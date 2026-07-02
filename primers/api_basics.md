# Primer — What is an API, and why researchers should care (10 min)

**Written for non-programmers. Read before Day 2, Session 4.**

When you use ChatGPT or Claude in the browser, you are using someone's *application*: a chat window wrapped around a model. An **API** (application programming interface) removes the wrapper — your code sends text to the model and gets text back, nothing else.

Why bother, when chat works fine? Three research reasons:

1. **Scale.** Classifying 800 survey answers by pasting them into a chat window is an afternoon of copy-paste and inconsistency. Via the API, it is a loop: same instruction, 800 inputs, 800 structured outputs, in minutes.
2. **Reproducibility.** A chat is a conversation — the model remembers earlier turns, the interface injects invisible instructions, and yesterday's chat can't be rerun. An API call is a self-contained request: the same input, model version, and settings can be sent again next month, by you or a reviewer. That's the difference between an anecdote and a method.
3. **Control.** The API exposes settings the chat hides. The one that matters most for us: **temperature** — how much randomness the model adds when choosing words. Temperature 0 ≈ "always pick the most likely answer" (maximally repeatable); higher values add variation. For coding/classification tasks you want repeatable, so you set it low and *report it*, like any instrument setting. You can also force **structured output** (e.g., valid JSON matching your schema), so 800 answers arrive as a clean table instead of 800 paragraphs.

**What an API call looks like** (Session 4 runs this together — you don't need to write it, you need to recognize its parts):

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",          # which model — report this
    contents=prompt + text_to_classify, # instruction + one input
    config={"temperature": 0, "response_mime_type": "application/json"},
)
```

**The API key** is the password attached to your account. Two rules, no exceptions: it lives in a secret store or environment variable, never inside code or documents; and if it ever appears in a chat, a repo, or a screenshot, you revoke it and make a new one (takes one minute — keys are disposable, your account's good standing is not).

**Cost mental model:** APIs charge per **token** (~¾ of a word). A 150-word survey answer + instructions ≈ 400 tokens in, 50 out. Classifying all 1,200 of our survey responses ≈ 0.5M tokens — on Gemini Flash's free tier: free; on paid tiers: a few cents. Compute *before* you run, then the number can't surprise you.
