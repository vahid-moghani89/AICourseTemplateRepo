#!/usr/bin/env bash
# For students WITHOUT a ChatGPT Plus or Claude Pro subscription (the "fallback" path).
# Run from the repo root:  bash check_agent.sh

set -u
KEYFILE="$HOME/.course_env"
if [ -f "$KEYFILE" ]; then
  # shellcheck disable=SC1090
  source "$KEYFILE"
fi

if [ -z "${GEMINI_API_KEY:-}" ]; then
  echo ""
  echo "No API key stored yet — run 'bash check_setup.sh' first (Block 0, Step 3)."
  echo ""
  exit 1
fi

echo ""
echo "Checking the fallback path..."
RESULT=$(python3 - <<'PYEOF' 2>&1
import course_utils
client = course_utils.get_client()
r = client.models.generate_content(model=course_utils.MODEL,
    contents="Reply with exactly: Fallback ready.")
print(r.text.strip())
PYEOF
)
if echo "$RESULT" | grep -q "Fallback ready"; then
  echo ""
  echo "Fallback ready — your key works. That is all you need before Day 3:"
  echo "we set up the fallback agent together in Session 5, and there is a"
  echo "backup plan on my side too. Nothing to buy, nothing more to install."
  if command -v gemini >/dev/null 2>&1; then
    echo ""
    echo "(Bonus: Google's 'gemini' command-line agent is already installed in"
    echo "your codespace as a fallback candidate — we test-drive it together in"
    echo "Session 5. Nothing to do now.)"
  fi
  echo ""
else
  echo ""
  echo "The key test failed — rerun 'bash check_setup.sh', and if it still"
  echo "fails, book a July-10 slot or email me. Error was: $RESULT"
  echo ""
fi
