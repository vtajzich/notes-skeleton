#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JIRA_DIR="$VAULT_ROOT/team-a/reference/jira"
PLUGIN="$HOME/.cursor/plugins/jira-tools/scripts"

FOLDERS="${1:-on-hold,selected-for-development,in-progress,done}"

echo "============================================"
echo " Full Jira Sync"
echo "============================================"
echo ""

echo ">>> Step 1/4: Refresh board status"
echo "--------------------------------------------"
bash "$PLUGIN/sync-jira-board.sh" --output-dir "$JIRA_DIR/"
echo ""

echo ">>> Step 2/4: Enhance issues (commits + stories)"
echo "--------------------------------------------"
export VAULT_ROOT
bash "$PLUGIN/enhance-jira-issues.sh" --output-dir "$JIRA_DIR/" --folders "$FOLDERS"
echo ""

echo ">>> Step 3/4: Rebuild index files"
echo "--------------------------------------------"
python3 "$PLUGIN/rebuild_index.py" "$JIRA_DIR/"
echo ""

echo ">>> Step 4/4: Map issues to product areas"
echo "--------------------------------------------"
python3 "$SCRIPT_DIR/map-jira-areas.py" "$JIRA_DIR/"
echo ""

echo "============================================"
echo " Full Jira Sync complete"
echo "============================================"
