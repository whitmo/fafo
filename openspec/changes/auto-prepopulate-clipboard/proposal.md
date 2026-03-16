## Why

When presenting a demo with showoff, the presenter has to type `next` before they can paste the first code block. This adds friction at the moment the audience is watching most closely — right when a step opens. The clipboard should already contain the first block, and each pasted command should automatically queue the next one.

## What Changes

- On subshell init, the first code block is immediately copied to the clipboard (no `next` needed)
- After pasting and executing a command, `next` is appended to the pasted text so it auto-runs, pre-loading the next block into the clipboard
- The presenter's workflow becomes: open step → paste → execute (block runs + next block loads) → paste → repeat

## Capabilities

### New Capabilities
- `auto-clipboard-prep`: Automatically prepopulate the clipboard on step entry and append `next` to pasted commands so the next block is queued after execution

### Modified Capabilities

## Impact

- `labs/showoff/bin/_shell-init.sh` — modify init sequence and `next` function to auto-copy first block and append `; next` to clipboard content
