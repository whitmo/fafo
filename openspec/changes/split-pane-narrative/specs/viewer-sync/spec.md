## ADDED Requirements

### Requirement: File-based synchronization between panes
The viewer SHALL watch the `.showoff-block-index` file and re-render when it changes.

#### Scenario: next command advances the block index
- **WHEN** the presenter runs `next` in the shell pane
- **THEN** the shell writes the new index atomically (write to temp file, mv into place) and the viewer re-renders within 0.5 seconds

#### Scenario: Rapid next invocations
- **WHEN** the presenter runs `next` multiple times in quick succession
- **THEN** the viewer debounces and renders only the final state, avoiding flicker

### Requirement: Viewer PID tracking
The viewer process PID SHALL be stored so the shell pane can detect viewer health.

#### Scenario: Viewer is healthy
- **WHEN** `next` checks the viewer PID and the process is alive
- **THEN** `next` proceeds normally (copy to clipboard, signal viewer)

#### Scenario: Viewer has crashed
- **WHEN** `next` checks the viewer PID and the process is not alive
- **THEN** `next` prints "Viewer stopped — continuing in single-pane mode" and skips viewer signaling for the rest of the step
