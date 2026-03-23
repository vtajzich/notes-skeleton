# Wrap Week

Generate a weekly wrap from the daily wraps of the target week.

## Instructions

1. Find all daily wraps in `wraps/YYYY/MM/Www/YYYY-MM-DD.md` for the target week
2. Read each daily wrap
3. Optionally read meeting notes directly if daily wraps are missing for some days
4. Generate a weekly wrap at `wraps/YYYY/MM/Www/week.md`

## Output Structure

```markdown
# Week WW — YYYY-MM-DD to YYYY-MM-DD
#work/wraps

## Executive Summary
2-3 sentence narrative of the week.

## Open Action Items
Table of all open items with Owner, Due, Source.

## Completed This Week
Checkbox list of items completed.

## Key Decisions
Table with Date, Decision, Context.

## Week Themes
3-5 named themes with one-sentence descriptions.

## Meetings This Week
Links to all meeting notes.

## Daily Wrap Sources
Links to each daily wrap consumed.
```
