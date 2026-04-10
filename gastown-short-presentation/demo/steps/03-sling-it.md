# Sling to Refinery

The mayor doesn't build — it delegates. Sling the bead to the conclave refinery.

```sh
gt sling <bead-id> conclave/refinery
```

The refinery will pick this up on its next hook check. No waiting, no confirmation.
It works in its own git worktree — isolated from the mayor's context.

```sh
gt hook conclave/refinery
```
