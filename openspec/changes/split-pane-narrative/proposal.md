## Why

In single-pane mode, the audience only sees terminal output — they miss the narrative context of what's being demonstrated and why. The presenter carries the entire story verbally. A split-pane mode shows the rendered step markdown alongside the shell, giving both presenter and audience a shared picture of where the demo is in its arc.

## What Changes

- Add optional `--split` flag to showoff that launches a tmux-based two-pane layout
- Left pane: narrative viewer that renders the active step's full markdown with progress tracking (completed/active/upcoming steps, highlighted current code block)
- Right pane: the existing interactive shell (unchanged)
- Left pane re-renders when `next` advances the block index
- Single-pane mode remains the default and works exactly as today
- Requires tmux as a dependency for split mode only

## Capabilities

### New Capabilities
- `split-pane-viewer`: tmux-based split layout with a narrative viewer pane that tracks demo progress and renders the active step's markdown with block highlighting
- `viewer-sync`: coordination between the shell pane (next/peek) and the viewer pane so the narrative tracks the presenter's position

### Modified Capabilities

## Impact

- `labs/showoff/bin/showoff` — add `--split` flag, tmux session management, pane lifecycle
- `labs/showoff/bin/_shell-init.sh` — `next` must signal the viewer pane to re-render after advancing
- New file: viewer script for the left pane (renders markdown with progress awareness)
- New dependency: tmux (split mode only; single-pane mode unchanged)
- Optional dependency: glow (for markdown rendering in the viewer)
