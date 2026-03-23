#!/usr/bin/env bash
set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$HOME/.cursor/plugins/jira-tools/scripts"

export VAULT_ROOT

bash "$PLUGIN/enhance-jira-issues.sh" --output-dir "$VAULT_ROOT/team-a/reference/jira/" "$@"
