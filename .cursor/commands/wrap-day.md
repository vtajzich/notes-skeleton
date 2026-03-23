# Wrap Day

Generate a daily wrap for the specified date.

## Instructions

1. Find all meeting notes from the target date across `**/meetings/**`
2. Read each meeting note
3. Generate a daily wrap at `wraps/YYYY/MM/Www/YYYY-MM-DD.md`

## Output Structure

```markdown
# Daily Wrap — YYYY-MM-DD
#work/wraps

## Quick Summary
- One bullet per meeting attended, capturing the key outcome

## Action Items
### Open
- All new open action items from today's meetings

### Completed
- Items marked done in today's meetings

## Key Points
- Non-actionable insights and decisions worth remembering

## Deadlines
| Item | Owner | Due | Source |
(only include if there are items with due dates within the next 2 weeks)

## Sources
- Links to each meeting note consumed
```

## Rules
- Follow the action-items rule for task format
- Follow the writing-style rule for tone and links
- Do not duplicate tasks that belong in Summary.md — reference them
