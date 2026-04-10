## 1. Viewer Script

- [x] 1.1 Create `bin/_viewer.sh` — bash loop that reads `.showoff-block-index`, renders active step via `glow` (fallback to `cat`), shows collapsed titles for non-active steps with ✓/▶/○ markers
- [x] 1.2 Add block highlighting pre-processing — awk/sed to dim completed blocks, highlight current block, and dim upcoming blocks before piping to `glow`
- [x] 1.3 Add step/block counter at bottom of viewer output (e.g., "Step 3/6 | Block 2/4")
- [x] 1.4 Store viewer PID in `$SHOWOFF_WORKSPACE/.showoff-viewer-pid` on startup

## 2. Split-Pane Launcher

- [x] 2.1 Add `--split` flag parsing to `bin/showoff`
- [x] 2.2 Add column-width guard: refuse below 100 cols, warn between 100-140 cols
- [x] 2.3 Add `$TMUX` detection — if inside tmux, use `tmux split-window -h`; if outside, create session with `tmux -L showoff`
- [x] 2.4 Launch viewer in left pane, shell in right pane, with proper env vars exported

## 3. Viewer-Shell Synchronization

- [x] 3.1 Update `_showoff_set_index` in `_shell-init.sh` to write atomically (write to temp file, `mv` into place)
- [x] 3.2 Add 0.5s poll loop in `_viewer.sh` — check `.showoff-block-index` mtime, re-render on change
- [x] 3.3 Add debounce to viewer re-render — skip intermediate states on rapid `next` invocations

## 4. Crash Recovery

- [x] 4.1 Add PID liveness check to `next` function — if viewer PID is dead, print "Viewer stopped — continuing in single-pane mode" and skip viewer signaling
- [x] 4.2 Kill viewer pane on shell exit (trap EXIT in subshell or in showoff main script after subshell returns)

## 5. Viz Code Blocks

- [x] 5.1 Add `viz` block detection to `_shell-init.sh` parser — skip `viz` blocks when building `_showoff_blocks` array (don't copy to clipboard)
- [x] 5.2 Add `viz` block execution in `_viewer.sh` — detect `viz` fenced blocks, execute the command, replace block with output in rendered markdown
- [x] 5.3 Add graceful fallback — if viz command not found, display raw command text with a note

## 6. Pane Lifecycle

- [x] 6.1 On step selection in main loop, export step info and signal viewer to re-render (update `.showoff-block-index` to 0)
- [x] 6.2 Ensure `--split` mode launches without `--split` behaving exactly as current single-pane mode (no regressions)
