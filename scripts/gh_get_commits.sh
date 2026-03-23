#!/usr/bin/env bash
set -euo pipefail

OWNER="YOUR_GITHUB_ORG"
LIMIT=1000

fail() { printf '  ✗ %s\n' "$1" >&2; exit 1; }

if [[ $# -ne 1 ]]; then
  printf 'Usage: %s <JIRA-KEY>\n' "$(basename "$0")" >&2
  printf 'Example: %s PROJ-1234\n' "$(basename "$0")" >&2
  exit 1
fi

JIRA_KEY="$1"

if [[ ! "$JIRA_KEY" =~ ^[A-Z]+-[0-9]+$ ]]; then
  fail "Invalid Jira key format: $JIRA_KEY (expected e.g. PROJ-1234)"
fi

command -v gh  &>/dev/null || fail "gh CLI not found. Install: https://cli.github.com"
command -v jq  &>/dev/null || fail "jq not found. Install: brew install jq"
gh auth token &>/dev/null || fail "gh CLI not authenticated. Run: gh auth login"

raw=$(gh search commits "$JIRA_KEY" \
  --owner "$OWNER" \
  --limit "$LIMIT" \
  --json sha,commit,repository)

total=$(printf '%s' "$raw" | jq 'length')
repos=$(printf '%s' "$raw" | jq '[.[].repository.fullName] | unique | length')

printf '%s' "$raw" | jq '[.[] | {
  sha:     .sha[0:8],
  date:    .commit.author.date,
  author:  .commit.author.name,
  repo:    .repository.fullName,
  message: .commit.message
}]'

printf 'Found %s commits for %s across %s repositories\n' "$total" "$JIRA_KEY" "$repos" >&2
