# A4 Option 4 — Interviewer starter app.
# The plumbing is done: chat UI, model calls, automatic transcript saving.
# YOUR work happens in system_prompt.md (your interview guide, encoded).
#
# Run:   streamlit run app.py        (from this folder, in your Codespace)
# Then:  Ports tab -> port 8501 -> visibility Public -> send the URL.

import datetime
import os
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

st.title("Research interview")
st.caption("You are talking with an AI interviewer, built for a course project. "
           "You can stop at any time. The anonymized transcript is used for coursework only.")

if "history" not in st.session_state:
    st.session_state.history = []           # list of {"role": ..., "text": ...}
    st.session_state.saved = False
    # Opening turn comes from the guide's opening/consent script:
    opening = client.models.generate_content(
        model=MODEL,
        config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.7},
        contents="Begin the interview now with your opening and consent script.",
    ).text
    st.session_state.history.append({"role": "interviewer", "text": opening})

for turn in st.session_state.history:
    with st.chat_message("assistant" if turn["role"] == "interviewer" else "user"):
        st.write(turn["text"])

def transcript_text() -> str:
    lines = [f"# Interview transcript — {datetime.datetime.now():%Y-%m-%d %H:%M}", ""]
    for t in st.session_state.history:
        who = "INTERVIEWER" if t["role"] == "interviewer" else "PARTICIPANT"
        lines += [f"**{who}:** {t['text']}", ""]
    return "\n".join(lines)

if user_msg := st.chat_input("Type your answer..."):
    st.session_state.history.append({"role": "participant", "text": user_msg})
    # Rebuild the conversation for the model:
    convo = []
    for t in st.session_state.history:
        role = "model" if t["role"] == "interviewer" else "user"
        convo.append({"role": role, "parts": [{"text": t["text"]}]})
    reply = client.models.generate_content(
        model=MODEL,
        config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.7},
        contents=convo,
    ).text
    st.session_state.history.append({"role": "interviewer", "text": reply})
    st.rerun()

if st.button("End interview & save transcript"):
    fname = TRANSCRIPTS / f"interview_{datetime.datetime.now():%Y%m%d_%H%M%S}.md"
    fname.write_text(transcript_text(), encoding="utf-8")
    st.session_state.saved = True
    st.success(f"Saved: {fname.name} — thank you! (Student: anonymize before committing.)")
