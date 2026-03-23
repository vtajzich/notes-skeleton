# AI-Managed Knowledge Base — Starter Template

A template repository for building a personal knowledge management system powered by AI agents and plain markdown files.

Instead of relying on a note-taking app's features, this system encodes your organizational conventions as **rules** and **commands** that an AI agent (Cursor, Windsurf, or similar) executes against plain text files. When your requirements change, you edit a rule — not a database schema, not a plugin config, not a template. The system adapts immediately.

See the article in [docs/article](docs/article/README.md)

## What's Inside

```
.cursor/
├── rules/          # How things should look — the AI reads these before every action
│   ├── vault-structure.mdc
│   ├── meeting-notes.mdc
│   ├── action-items.mdc
│   └── writing-style.mdc
└── commands/       # What to do — repeatable workflows you trigger on demand
    ├── wrap-day.md
    ├── wrap-week.md
    ├── wrap-month.md
    ├── wrap-quarter.md
    ├── summarize-1on1.md
    └── triage-tasks.md

team-a/             # Your team — products, meetings, reference docs
├── team.md
├── product-x/
├── product-y/
├── meetings/
│   ├── 1-on-1-alice/
│   ├── 1-on-1-bob/
│   ├── weekly-sync/
│   └── adhoc/
└── reference/
    └── jira/       # Local Jira mirror (populated by scripts)

initiatives/        # Time-bound strategic goals
people/             # Person profiles (JSON + markdown pairs)
wraps/              # Time-based rollups: daily → weekly → monthly → quarterly

scripts/            # Automation
├── full-jira-sync.sh       # Pull Jira issues + comments + commits into markdown
├── gh_get_commits.sh       # Find GitHub commits by Jira key
├── encrypt.sh / decrypt.sh # Encrypt sensitive notes before git commit
├── setup.sh                # One-time setup for encryption + git hooks
├── check_links.py          # Find broken internal links
└── convert_wikilinks.py    # Convert [[wikilinks]] to standard markdown links

Todos.md            # Aggregated task list built by triage-tasks command
.secure             # Patterns for directories to encrypt (e.g. 1-on-1-*)
```

## How It Works

1. **Write meeting notes** — drop them in the appropriate `meetings/` folder using `YYYY-MM-DD.md` naming
2. **Run commands** — `wrap-day` generates a daily summary, `summarize-1on1` updates a 1-on-1 Summary.md, `triage-tasks` rebuilds your task list
3. **Read the output** — wraps give you a time-based view (daily → quarterly), Summary.md files give you a per-meeting-series view
4. **Change the rules** — when something isn't working, describe what you want differently and let the AI update the rule

## Getting Started

1. **Clone this repo**
   ```bash
   git clone <this-repo> my-notes
   cd my-notes
   ```

2. **Set up encryption** (optional, for sensitive notes like 1-on-1s)
   ```bash
   ./scripts/setup.sh
   ```

3. **Open in Cursor** (or any AI agent environment that reads `.cursor/rules/`)

4. **Start writing meeting notes** — the AI already knows your conventions from the rules

5. **Run your first command** — try `wrap-day` to generate a daily wrap from today's notes

## Adapting to Your Workflow

This template reflects one person's mental model. **It doesn't have to match yours.**

- Rename `team-a/` to your actual team or area
- Add or remove product directories
- Change meeting note structure in `.cursor/rules/meeting-notes.mdc`
- Modify the action item format in `.cursor/rules/action-items.mdc`
- Edit commands to change what gets generated and how

The rules are plain English (or any language — the AI doesn't care). Describe your conventions, and the AI follows them. When your conventions evolve, edit the rule. No migrations, no rebuilding templates.

## Jira Integration

The scripts assume a Cursor plugin for Jira sync (`$HOME/.cursor/plugins/jira-tools/`). To use the Jira mirror:

1. Update `YOUR_GITHUB_ORG` in `scripts/gh_get_commits.sh` to your GitHub organization
2. Configure the Jira plugin with your board and credentials
3. Run `scripts/full-jira-sync.sh` to pull issues, comments, and related commits

## Encryption

Directories matching patterns in `.secure` are automatically encrypted before git commit and decrypted after pull. Uses AES-256-CBC via OpenSSL. The encryption key is stored in your shell environment, not in the repo.

By default, `1-on-1-*` directories are encrypted. Edit `.secure` to add or remove patterns.

## Background

This template accompanies the article [I Stopped Using Note-Taking Apps. Now an AI Agent Manages My Knowledge Base.](https://medium.com/@v.tajzich/my-notes-are-always-current-not-because-im-organized-3f2be972cff6) on Medium.

The example content tells a coherent story (API gateway migration, developer portal search, onboarding v2, incident debrief) to demonstrate how notes, summaries, wraps, tasks, and people profiles connect across the system.
