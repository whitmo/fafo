## Context

Showoff is a bash+gum demo runner. It currently works in single-pane mode: gum step list, then a subshell with `next`/`peek` commands. The user wants an optional split-pane mode where a narrative viewer sits alongside the shell.

An adversarial review raised concerns about projector column limits, nested tmux, and pane crash recovery. A counter-review argued these are solvable and that screen-sharing (not projectors) is the dominant presentation context. Both are incorporated below.

## Goals / Non-Goals

**Goals:**
- Opt-in `--split` mode with vertical two-pane layout (narrative left, shell right)
- Narrative pane renders the active step's full markdown with progress tracking
- Graceful handling of tmux nesting, terminal width constraints, and pane crashes
- Support for inline data visualization in step markdown (sparklines, progress bars)
- Single-pane mode unchanged and remains the default

**Non-Goals:**
- Rewriting showoff in Go/Python — this stays bash
- Supporting non-tmux terminal splits in v1 (kitty/WezTerm is a future enhancement)
- Auto-executing code blocks — presenter always explicitly runs commands
- Live system metric collection (the markdown author can embed metric commands, but showoff doesn't instrument the system)

## Decisions

**Use tmux for pane management, with `$TMUX` detection**

If `$TMUX` is set, use `tmux split-window -h` within the existing session. If not, create a new session with `tmux -L showoff` (dedicated socket to avoid conflicts). This avoids nested tmux entirely.

Alternative considered: kitty/WezTerm native splits. Deferred to future — tmux has broadest compatibility and the `$TMUX` detection pattern handles the nesting problem cleanly.

**Viewer is a bash loop script (`_viewer.sh`) that watches `.showoff-block-index`**

The viewer runs in the left pane. On each render cycle:
1. Clear the pane
2. Show collapsed step titles with completion markers (✓/▶/○)
3. For the active step, render full markdown via `glow` with ANSI injection for block highlighting
4. Show step/block counter at bottom

Re-render triggers: poll `.showoff-block-index` mtime every 0.5s. When it changes, re-render. This is simpler than named pipes or inotify and has acceptable latency for a presentation context.

Alternative considered: named pipe (fifo) for instant signaling. More complex, harder to debug, marginal benefit since 0.5s polling is imperceptible during a talk.

**Block highlighting via sed pre-processing before glow**

Rather than building a custom markdown renderer, pre-process the markdown file before piping to `glow`:
- Wrap the current code block in a visual marker (e.g., add `> ` prefix or inject ANSI escape sequences)
- Dim completed blocks (inject dim ANSI codes)
- Pass the modified markdown to `glow` for rendering

This is ~20 lines of awk/sed, not a custom renderer.

**Column-width guard at launch**

`tput cols` check before launching split mode. Below 140 columns: print a warning. Below 100 columns: refuse and suggest single-pane mode. This addresses the projector scenario without blocking screen-sharing users who have ample width.

**Crash recovery via PID check**

The viewer's PID is stored in `$SHOWOFF_WORKSPACE/.showoff-viewer-pid`. The `next` function checks if this PID is alive. If dead: print a message ("viewer crashed, continuing in single-pane mode") and skip further viewer signals. The showoff main script also checks on step completion and offers to restart.

**Inline data viz via shell-executable code blocks**

Step markdown can include fenced blocks tagged with `viz` instead of `sh`:
````markdown
```viz
spark 0 30 55 80 33 150
```
````

The viewer script detects `viz` blocks and executes them inline during rendering (output replaces the block). This enables sparklines, progress bars, or plotext charts embedded in the narrative. `viz` blocks are NOT copied to clipboard by `next` — they are viewer-only.

## Risks / Trade-offs

- [Polling latency] → 0.5s is imperceptible during a presentation. Can be reduced if needed.
- [glow not installed] → Fallback to `cat` with manual ANSI highlighting. Functional but less pretty.
- [`viz` block execution in viewer] → Security consideration: only execute in trusted demo content (which is author-controlled). No user-input risk since step files are static.
- [tmux dependency for split mode] → Acceptable since it's opt-in and tmux is widely available.
- [`; next` visible to audience] → Acknowledged tradeoff from the auto-clipboard change. Reinforces the flow but is a visible implementation detail. Revisit if audience feedback is negative.
