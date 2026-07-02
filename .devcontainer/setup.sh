#!/usr/bin/env bash
# Course environment setup. Runs automatically when the codespace is created.
# Safe to rerun anytime:  bash .devcontainer/setup.sh

echo ""
echo "================================================================"
echo "  Course setup starting — 4 steps, usually 4–8 minutes total."
echo "  You will see progress below. Slow is normal; silent is not."
echo "================================================================"

echo ""
echo "--- Step 1/4: Python packages (the longest step, 2–5 min) ---"
timeout 600 pip install -r requirements.txt \
  && echo "--- Step 1/4 done ---" \
  || echo "!!! Step 1 had trouble — run 'bash .devcontainer/setup.sh' again, or continue; check_setup.sh will tell you what's missing."

echo ""
echo "--- Step 2/4: Codex CLI (terminal agent, ~1 min) ---"
timeout 180 npm install -g @openai/codex </dev/null \
  && echo "--- Step 2/4 done ---" \
  || echo "!!! Codex CLI skipped (the sidebar extension covers you; the CLI can be added in Session 5)."

echo ""
echo "--- Step 3/4: Claude Code CLI (terminal agent, ~1 min) ---"
timeout 180 bash -c 'curl -fsSL https://claude.ai/install.sh | bash' </dev/null \
  && echo "--- Step 3/4 done ---" \
  || echo "!!! Claude Code CLI skipped (the sidebar extension covers you; the CLI can be added in Session 5)."

echo ""
echo "--- Step 4/4: Gemini CLI (fallback candidate, ~1 min) ---"
timeout 180 npm install -g @google/gemini-cli </dev/null \
  && echo "--- Step 4/4 done ---" \
  || echo "!!! Gemini CLI skipped (only relevant for the fallback path; Session 5 has a backup)."

echo ""
echo "================================================================"
echo "  Setup finished."
echo ""
echo "  IMPORTANT: this window is the BUILD LOG — it stays like this"
echo "  and will not turn into a normal terminal. That is normal."
echo "  To start working: open a FRESH terminal (menu at top-left ->"
echo "  Terminal -> New Terminal) and run:  bash check_setup.sh"
echo ""
echo "  Any '!!!' lines above? Rerunning this script usually fixes them:"
echo "  bash .devcontainer/setup.sh"
echo "================================================================"
echo ""
