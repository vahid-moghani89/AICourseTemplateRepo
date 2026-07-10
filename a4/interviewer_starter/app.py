# A4 Option 4 — Interviewer starter app.
# The plumbing is done: chat UI, model calls, automatic transcript saving,
# and graceful handling of rate limits mid-interview.
# YOUR work happens in system_prompt.md (your interview guide, encoded).
#
# Run:   streamlit run app.py        (from this folder, in your Codespace)
# Then:  Ports tab -> port 8501 -> visibility Public -> send the URL.

import datetime
import time
import pathlib

import streamlit as st

HERE = pathlib.Path(__file__).parent
SYSTEM_PROMPT = (HERE / "system_prompt.md").read_text(encoding="utf-8")
TRANSCRIPTS = HERE / "transcripts"
TRANSCRIPTS.mkdir(exist_ok=True)

import sys
sys.path.append(str((HERE / ".." / "..").resolve()))  # repo root
import course_utils

try:
    client = course_utils.get_client()
except RuntimeError as e:
    st.error(f"API key problem — in the terminal, run:  bash check_setup.sh  (from the repo root), then restart this app. Details: {e}")
    st.stop()

MODEL = course_utils.MODEL

# The conversation sent to the model must START with a user turn — this
# kickoff line plays that role and never appears in the visible chat.
KICKOFF = "Begin the interview now with your opening and consent script."


def interviewer_reply(convo):
    """One model call with polite rate-limit handling. If the free tier's
    meter trips mid-interview, we wait once and retry; the participant sees
    a calm message instead of a crash, and the transcript is never lost."""
    for attempt in (1, 2):
        try:
            r = client.models.generate_content(
                model=MODEL,
                config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.7},
                contents=convo,
            )
            return r.text
        except Exception as e:
            if ("429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)) and attempt == 1:
                with st.spinner("One moment — the interviewer is catching its breath (about 30 seconds)..."):
                    time.sleep(30)
            else:
                raise


def build_convo():
    """History as the API expects it: starts with the hidden user kickoff."""
    convo = [{"role": "user", "parts": [{"text": KICKOFF}]}]
    for t in st.session_state.history:
        role = "model" if t["role"] == "interviewer" else "user"
        convo.append({"role": role, "parts": [{"text": t["text"]}]})
    return convo


def transcript_text() -> str:
    lines = [f"# Interview transcript — {datetime.datetime.now():%Y-%m-%d %H:%M}", ""]
    for t in st.session_state.history:
        who = "INTERVIEWER" if t["role"] == "interviewer" else "PARTICIPANT"
        lines += [f"**{who}:** {t['text']}", ""]
    return "\n".join(lines)


def autosave():
    """Write the transcript to disk after every turn — a crash, a closed tab,
    or a slept Codespace can no longer lose an interview."""
    st.session_state.autosave_path.write_text(transcript_text(), encoding="utf-8")


st.title("Research interview")
st.caption("You are talking with an AI interviewer, built for a course project. "
           "You can stop at any time. The anonymized transcript is used for coursework only.")

if "history" not in st.session_state:
    st.session_state.history = []           # list of {"role": ..., "text": ...}
    st.session_state.autosave_path = TRANSCRIPTS / f"interview_{datetime.datetime.now():%Y%m%d_%H%M%S}.md"
    try:
        opening = interviewer_reply([{"role": "user", "parts": [{"text": KICKOFF}]}])
    except Exception as e:
        st.error("The interviewer could not start. Researcher: check the terminal — "
                 f"likely the daily rate limit or the API key. Details: {e}")
        st.stop()
    st.session_state.history.append({"role": "interviewer", "text": opening})
    autosave()

for turn in st.session_state.history:
    with st.chat_message("assistant" if turn["role"] == "interviewer" else "user"):
        st.write(turn["text"])

if user_msg := st.chat_input("Type your answer..."):
    st.session_state.history.append({"role": "participant", "text": user_msg})
    autosave()
    try:
        reply = interviewer_reply(build_convo())
        st.session_state.history.append({"role": "interviewer", "text": reply})
        autosave()
    except Exception:
        autosave()
        st.warning("The interviewer hit a technical limit and needs a longer pause — "
                   "this is not your fault, and everything you said is saved. "
                   "The researcher will be in touch to continue or reschedule.")
    st.rerun()

if st.button("End interview & save transcript"):
    autosave()
    st.success(f"Saved: {st.session_state.autosave_path.name} — thank you! "
               "(Student: anonymize before committing.)")
