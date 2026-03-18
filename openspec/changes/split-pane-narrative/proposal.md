## Why

In single-pane mode, the audience only sees terminal output — they miss the narrative context of what's being demonstrated and why. The presenter carries the entire story verbally. A split-pane mode shows the rendered step markdown alongside the shell, giving both presenter and audience a shared picture of where the demo is in its arc.

## What Changes

- Add optional `--split` flag to showoff that launches a two-pane layout (vertical split: left = narrative, right = shell)
- Left pane: narrative viewer that renders the active step's full markdown with progress tracking (completed/active/upcoming steps, highlighted current code block)
- Right pane: the existing interactive shell (unchanged)
- Left pane re-renders when `next` advances the block index
- Single-pane mode remains the default and works exactly as today
- Pane management: detect `$TMUX` and split within existing session, otherwise create a new tmux session. Future: support kitty/WezTerm native splits.
- Markdown files can embed inline data viz (sparklines via `spark`, charts via `plotext`) for richer narrative content

## Capabilities

### New Capabilities
- `split-pane-viewer`: two-pane layout with a narrative viewer that tracks demo progress and renders the active step's markdown with block highlighting. Vertical split is the primary layout. Supports tmux (detect existing session vs create new), with future extensibility for native terminal splits (kitty, WezTerm).
- `viewer-sync`: coordination between the shell pane (next/peek) and the viewer pane via file-based signaling on `.showoff-block-index`. Viewer watches the index file and re-renders on change. Writes must be atomic (write to temp, mv into place). Viewer debounces rapid updates.
- `narrative-viz`: support for inline terminal visualizations in step markdown — sparklines (via `spark`), progress bars (pure bash), and optional richer charts (via `plotext`). These render in the narrative pane alongside prose.

### Modified Capabilities

## Impact

- `labs/showoff/bin/showoff` — add `--split` flag, `$TMUX` detection, tmux session/pane lifecycle, column-width guard (warn <140 cols, refuse <100)
- `labs/showoff/bin/_shell-init.sh` — `next` must signal the viewer pane to re-render (atomic write to index file). Detect viewer process liveness; if dead, degrade to single-pane with a message.
- New file: `labs/showoff/bin/_viewer.sh` — left pane viewer script. Renders active step via `glow` with pre-processing to highlight the current code block and dim completed ones. Shows collapsed titles for non-active steps with completion markers.
- New dependency: tmux (split mode only; single-pane mode unchanged)
- Optional dependencies: glow (markdown rendering), spark (inline sparklines), plotext (richer charts)

## Guardrails

- `$TMUX` detection: if already in tmux, use `tmux split-window` in existing session (no nesting). If not, create a dedicated session.
- Column check: `tput cols` before launching split. Warn below 140, refuse below 100 with suggestion to use single-pane mode.
- Crash recovery: if the viewer pane process dies, `next` detects it (check PID) and either restarts the viewer or prints a message and continues in single-pane mode. Never leave a dead pane on screen.
- `--split` is opt-in. Single-pane default is preserved for constrained environments (projectors, small terminals).
