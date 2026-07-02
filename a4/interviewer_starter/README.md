# Interviewer starter (A4, Option 4)

The plumbing — chat interface, model calls, automatic transcript saving — is done. Your work is `system_prompt.md`: replace every bracketed part with your interview guide. That file *is* the interviewer; writing it well is the assignment.

## Run it

1. In your Codespace terminal, from this folder: `streamlit run app.py`
2. Open the **Ports** tab (next to the terminal) → port **8501** → right-click → *Port visibility* → **Public** → copy the URL.
3. Open that URL on another device (your phone) — that's your dry-run test, and later the link you send participants.
4. Every interview ends with the **End interview & save transcript** button — transcripts land in `transcripts/`, one file per interview. **Anonymize before committing** (names → P1, P2…; the Survival Kit reminds you why: git remembers forever).

## Three things to know

- The app reads your API key from the environment (`check_setup.sh` stored it) — the key never appears in the browser or the code.
- Keep the Codespace tab open during interviews; a sleeping Codespace means a frozen interview.
- Lane B: hand this folder, your interview guide, and the behavioral rules to your agent and direct the adaptation — the starter is deliberately minimal so there's real directing to do (e.g., a nicer ending flow, participant ratings built in).
