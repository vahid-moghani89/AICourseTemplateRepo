# Primer — What is an AI agent? (5 min)

**Read before Day 3.**

A chatbot answers; an **agent acts**. Technically, an agent is the same kind of model you've been chatting with, placed in a loop and given tools: it can read your files, write files, run code, see the result, and decide what to do next — repeating until it judges the task done or asks you something.

That loop is what changes the experience. You say "explore this dataset and summarize its problems," and instead of an answer *about* how one might do that, the agent opens the CSV, runs checks, hits an error, reads the error, fixes its own code, and hands you a summary — with the files it created sitting in your project.

**What it can touch — and what it can't.** The agents in this course run inside your Codespace: a disposable computer in the cloud containing only the course repository. The agent can read, write, and execute *there*. It cannot reach your laptop, your email, your university drive, or your real research data — those aren't in the box. This containment is not an accident; it's the first thing to check whenever you use an agent anywhere else.

**The three rules** (Session 6 drills them; A3 grades them):

1. **Specify before you delegate.** An agent amplifies your instructions, including the vague ones. The craft is writing down — *before* starting — what the inputs are, what outputs you expect, and how you'll check them (acceptance criteria). A vague spec doesn't fail loudly; it produces something plausible and wrong.
2. **Watch it work — in checkpoints.** Don't approve a 14-step plan and walk away. Gate the work: plan first, then cleaning, then analysis — and inspect the intermediate state at each gate. You're the PI; the agent is an eager, fast, occasionally overconfident assistant.
3. **Verify like a reviewer.** The agent's confidence carries no information. Recompute a number independently, trace a few records end-to-end, read the code it wrote (or make it explain every line — it's good at that). What survives your verification is yours to sign.

**Vocabulary you'll meet on Day 3:** *context file* (`AGENTS.md` / `CLAUDE.md` — a markdown file in the repo that the agent reads automatically: your project description and standing instructions); *session log* (the transcript of everything the agent did — in research use, that's documentation gold); *diff* (the exact before/after of every file change — your primary review surface).

One more thing: the skills here are not programming skills. Specifying tasks precisely, gating work, verifying against criteria — that's supervision. If you've ever managed a research assistant, you already know the job; the assistant just got faster and more literal.
