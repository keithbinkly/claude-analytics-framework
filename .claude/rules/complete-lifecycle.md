# Complete Full Lifecycle

## The Pattern

When processing items from a queue, list, batch, or intake pipeline: always complete the FULL lifecycle. Process the items AND update their status.

## Required Steps

1. **Process** the items (whatever the action is)
2. **Move/update status** — mark as done, move from intake to processed, check off the list
3. **Verify** — confirm the source list reflects the changes

## Anti-Pattern

```
WRONG: Process 53 resources → leave them all in the intake queue → user discovers nothing was moved
RIGHT: Process 53 resources → move each to processed section → confirm intake is empty
```

## Applies To

- Resource intake queues
- Migration checklists
- Batch file operations (rename, move, archive)
- Todo lists and dot files
- Any list where items have a "pending → done" lifecycle

## Why

Processed items left in a pending state create confusion, duplicate work, and erode trust. The processing isn't done until the bookkeeping is done.
