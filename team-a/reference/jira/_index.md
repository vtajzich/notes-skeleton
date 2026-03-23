# Jira Mirror
#work/team-a/jira

> Last synced: (not yet synced) | Run `scripts/full-jira-sync.sh` to populate

This directory contains a local mirror of Jira issues, organized by board status.

## Status Folders

| Folder | Board Column |
|---|---|
| `backlog/` | Backlog |
| `selected-for-development/` | Selected for Development |
| `in-progress/` | In Progress |
| `on-hold/` | On Hold |
| `done/` | Done |

## How It Works

1. `sync-jira.sh` pulls issues from Jira and writes one markdown file per issue
2. `enhance-jira.sh` enriches each issue with GitHub commits and Jira comments
3. `rebuild-jira-index.sh` regenerates the `_index.md` in each status folder
4. `map-jira-areas.py` classifies issues by product area using heuristic rules

Run `scripts/full-jira-sync.sh` to execute all four steps in sequence.
