#!/usr/bin/env bash
# Course data sync — run this once from your repo's root folder (the Codespace terminal):
#
#   bash sync_data.sh
#
# Why: the course datasets were replaced on 10 July 2026. If you made your copy of the
# template before that, your data/ folder is stale and your A3 results will not match
# the graded dataset. This script downloads the current files and verifies them.
set -euo pipefail

BASE="https://raw.githubusercontent.com/vahid-moghani89/AICourseTemplateRepo/main"

SURVEY_SHA="3b4c2f9c656f3f4d699a3702252a70b21cfd937eaa78c703622578faefa223f9"
SAMPLE_SHA="90cc0453f884a143deee670ddf26ce9bae6c207255ccfb1d9c0516af527ad746"

if [ ! -d "data" ]; then
  echo "!!! Run this from your repo's root folder (where the data/ folder is)."
  echo "    In a Codespace: cd /workspaces/<your-repo-name> && bash sync_data.sh"
  exit 1
fi

echo "Downloading current course data ..."
mkdir -p data/synthetic_survey
curl -fsSL "$BASE/data/synthetic_survey/survey.csv" -o data/synthetic_survey/survey.csv
curl -fsSL "$BASE/data/sample_200.csv" -o data/sample_200.csv

echo "Verifying ..."
check() {
  local file="$1" want="$2"
  local got
  got=$(sha256sum "$file" | cut -d' ' -f1)
  if [ "$got" = "$want" ]; then
    echo "  OK   $file"
  else
    echo "  FAIL $file — download looks wrong or interrupted. Run the script again;"
    echo "       if it fails twice, post on the Discussions board."
    exit 1
  fi
}
check data/synthetic_survey/survey.csv "$SURVEY_SHA"
check data/sample_200.csv "$SAMPLE_SHA"

rows=$(($(wc -l < data/synthetic_survey/survey.csv) - 1))
echo ""
echo "All good: survey.csv ($rows rows) and sample_200.csv are current."
echo "If your repo also has an instructor/ folder: it was included by mistake and is"
echo "obsolete — delete it (right-click > Delete in the Explorer, then commit)."
echo "Remember to commit: git add data/ && git commit -m 'sync course data' && git push"
