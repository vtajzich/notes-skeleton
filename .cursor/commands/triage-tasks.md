# Triage Tasks

Scan all Summary.md files and rebuild the prioritized task list.

## Instructions

1. Find all `**/Summary.md` files in the vault
2. Extract all open action items (`- [ ]`)
3. Group by owner, then by priority
4. Write the result to `Todos.md` at the vault root

## Output Structure

```markdown
# My Todos
#work

> Last refreshed: YYYY-MM-DD

## My Tasks
### High Priority
(items assigned to @Me with ⏫)

### In Progress
(items currently being worked on)

### Other
(remaining @Me items)

## Delegated
### {Person Name}
(items assigned to others, grouped by person)

## Completed Since Last Refresh
(items completed since the previous refresh date)
```
