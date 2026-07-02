#!/usr/bin/env bash
# Block 0 verification. Run from the repo root:  bash check_setup.sh
# Friendly by design: every failure says what to do next.

set -u
PASS=0; FAIL=0
ok()   { echo "  [OK]   $1"; PASS=$((PASS+1)); }
bad()  { echo "  [FIX]  $1"; FAIL=$((FAIL+1)); }

echo ""
echo "Checking your course environment..."
echo ""

# 1. Python + packages
if python3 -c "import sys; assert sys.version_info >= (3,11)" 2>/dev/null; then
  ok "Python 3.11+ found"
else
  bad "Python 3.11+ not found — in a Codespace this should not happen; email me a screenshot"
fi
for pkg in google.genai pandas sklearn streamlit; do
  if python3 -c "import $pkg" 2>/dev/null; then
    ok "package '$pkg' installed"
  else
    bad "package '$pkg' missing — run: pip install -r requirements.txt"
  fi
done

# 2. Course files
for f in data/synthetic_survey/survey.csv data/sample_200.csv data/codebook_concerns.md templates/ai_use_log.md notebooks/api_check.ipynb; do
  if [ -f "$f" ]; then ok "file '$f' present"; else bad "file '$f' missing — did you create your repo with 'Use this template'?"; fi
done

# 3. API key (stored in ~/.course_env so it never enters the repo)
KEYFILE="$HOME/.course_env"
if [ -f "$KEYFILE" ] && grep -q GEMINI_API_KEY "$KEYFILE"; then
  ok "API key already stored"
  # shellcheck disable=SC1090
  source "$KEYFILE"
  # older installs stored only one name for the key — add the second (the
  # gemini CLI looks for GOOGLE_API_KEY; python tools use GEMINI_API_KEY):
  if ! grep -q GOOGLE_API_KEY "$KEYFILE"; then
    echo "export GOOGLE_API_KEY=\"$GEMINI_API_KEY\"" >> "$KEYFILE"
    source "$KEYFILE"
    ok "key also stored under GOOGLE_API_KEY (for the gemini CLI)"
  fi
else
  echo ""
  echo "  Paste your API key from Block 0 Step 2 (Vertex or AI Studio)."
  echo "  It will be stored in $KEYFILE — outside the repo, so it can never be committed."
  read -r -s -p "  API key: " APIKEY; echo ""
  echo "export GEMINI_API_KEY=\"$APIKEY\"" > "$KEYFILE"
  echo "export GOOGLE_API_KEY=\"$APIKEY\"" >> "$KEYFILE"
  chmod 600 "$KEYFILE"
  grep -q "source $KEYFILE" "$HOME/.bashrc" 2>/dev/null || echo "source $KEYFILE" >> "$HOME/.bashrc"
  source "$KEYFILE"
  ok "API key stored"
fi

# 4. Live API test (tries both Google endpoints — Vertex and Developer API —
#    and remembers which one your key belongs to)
echo ""
echo "  Testing your key with a real model call (a few seconds)..."
RESULT=$(python3 - <<'PYEOF' 2>&1
import course_utils
client = course_utils.get_client(verbose=True)
r = client.models.generate_content(model=course_utils.MODEL,
    contents="Reply with exactly: API check passed.")
print(r.text.strip())
PYEOF
)
if echo "$RESULT" | grep -q "API check passed"; then
  ok "live API call works"
  echo "$RESULT" | grep "Connected via" | sed 's/^/         /'
else
  bad "API call failed. If the details mention a mistyped or invalid key: delete $KEYFILE and rerun this script with a freshly copied key. Otherwise the message below says what to do."
  echo "$RESULT" | sed 's/^/         /'
fi

echo ""
if [ "$FAIL" -eq 0 ]; then
  echo "All checks passed — see you on July 13."
else
  echo "$FAIL item(s) to fix (marked [FIX] above). Stuck for more than 10 minutes? Book a July-10 slot or email me."
fi
echo ""
