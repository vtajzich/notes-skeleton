#!/usr/bin/env bash
set -euo pipefail
VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$HOME/.cursor/plugins/jira-tools/scripts"
bash "$PLUGIN/sync-jira-board.sh" --output-dir "$VAULT_ROOT/team-a/reference/jira/"
