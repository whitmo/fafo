## Context

Showoff is a bash+gum demo runner. When a presenter selects a step, a subshell opens via `bash --rcfile _shell-init.sh`. Currently, the presenter must type `next` to get the first code block into the clipboard. Each subsequent `next` call copies one block at a time.

The goal is zero-friction presenting: open a step, paste, execute, paste, execute — no typing `next` between blocks.

## Goals / Non-Goals

**Goals:**
- First code block is in the clipboard the moment the subshell opens
- After pasting a command, the next block is automatically queued in the clipboard
- Presenter never types `next` during normal flow

**Non-Goals:**
- Changing the `peek` command behavior
- Auto-executing code blocks (presenter must always explicitly paste and run)
- Handling non-shell code blocks differently

## Decisions

**Append `; next` to clipboard content rather than using shell hooks (PROMPT_COMMAND, trap DEBUG, etc.)**

Rationale: Shell hooks are fragile — `PROMPT_COMMAND` fires on every prompt (even empty enters), `trap DEBUG` fires before every command. Both would cause false triggers. Appending `; next` to the clipboard content is simple and predictable: when the presenter pastes, the original command runs, then `next` runs and loads the next block. No magic.

Trade-off: The `; next` is visible in the terminal when pasted. This is acceptable — it's a demo tool and seeing `next` reinforces the flow to the audience.

**Auto-copy first block during shell init, not in showoff main script**

Rationale: Keeps the clipboard logic in one place (`_shell-init.sh`). The main script doesn't need to know about clipboard behavior.

## Risks / Trade-offs

- [Multiline blocks with `; next` appended] → `; next` appends after the last line, which works correctly for both single-line and multiline commands
- [Last block in a step still appends `; next`] → `next` will print "No more code blocks" which is a natural signal to exit. No harm done.
