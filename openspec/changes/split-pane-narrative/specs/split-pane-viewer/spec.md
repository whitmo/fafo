## ADDED Requirements

### Requirement: Split-pane layout via --split flag
Showoff SHALL support a `--split` flag that launches a vertical two-pane layout with the narrative viewer on the left and the interactive shell on the right.

#### Scenario: Launch with --split in a non-tmux terminal
- **WHEN** the user runs `showoff --split ./steps ./workspace` outside of tmux
- **THEN** showoff creates a new tmux session with a dedicated socket (`tmux -L showoff`) and splits it into two panes

#### Scenario: Launch with --split inside an existing tmux session
- **WHEN** the user runs `showoff --split ./steps ./workspace` inside an existing tmux session (`$TMUX` is set)
- **THEN** showoff uses `tmux split-window -h` within the current session (no nesting)

#### Scenario: Launch without --split
- **WHEN** the user runs `showoff ./steps ./workspace` without `--split`
- **THEN** showoff behaves exactly as the current single-pane mode

### Requirement: Column-width guard
Showoff SHALL check terminal width before launching split mode and warn or refuse if insufficient.

#### Scenario: Terminal width below 100 columns
- **WHEN** `tput cols` returns less than 100 and `--split` is requested
- **THEN** showoff refuses to launch split mode and suggests using single-pane mode

#### Scenario: Terminal width between 100 and 140 columns
- **WHEN** `tput cols` returns between 100 and 140 and `--split` is requested
- **THEN** showoff prints a warning about limited space and proceeds

### Requirement: Narrative viewer renders active step
The left pane viewer SHALL render the active step's full markdown with visual distinction between completed, current, and upcoming code blocks.

#### Scenario: Active step with multiple code blocks
- **WHEN** the viewer renders a step that has 3 code blocks and the presenter is on block 2
- **THEN** block 1 is visually dimmed, block 2 is highlighted, and block 3 is visually dimmed

#### Scenario: Non-active steps shown as collapsed titles
- **WHEN** the viewer renders the step list
- **THEN** completed steps show as `✓ Title`, the active step is expanded with full markdown, and upcoming steps show as `○ Title`

### Requirement: Pane lifecycle management
Showoff SHALL manage the viewer pane lifecycle across step transitions.

#### Scenario: Step selection updates the viewer
- **WHEN** the presenter selects a new step from the step list
- **THEN** the viewer pane updates to show the newly selected step's content

#### Scenario: Viewer pane process crashes
- **WHEN** the viewer process dies unexpectedly during a demo
- **THEN** the `next` command detects the dead process and prints a message indicating single-pane fallback, and the shell pane continues to function normally

#### Scenario: Exiting the shell pane
- **WHEN** the presenter exits the shell pane (types `exit` or ctrl-d)
- **THEN** the viewer pane is killed and the presenter returns to the step list
