#!/usr/bin/env bash
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$HOME/.cursor/plugins/jira-tools/scripts"

echo "Rebuilding Jira index files..."
python3 "$PLUGIN/rebuild_index.py" "$VAULT_ROOT/team-a/reference/jira/"
