## ADDED Requirements

### Requirement: Auto-copy first block on step entry
When a step's subshell opens, the first code block from the step's markdown SHALL be automatically copied to the clipboard without the presenter typing any command.

#### Scenario: Step with code blocks opens
- **WHEN** a presenter selects a step and the subshell initializes
- **THEN** the first code block is copied to the clipboard and displayed in the terminal

#### Scenario: Step with no code blocks opens
- **WHEN** a presenter selects a step that has no code blocks
- **THEN** no clipboard action occurs and a message indicates there are no blocks

### Requirement: Next block auto-queued after paste
The `next` command output copied to the clipboard SHALL have `; next` appended so that pasting and executing a block automatically loads the next block.

#### Scenario: Pasting a single-line block
- **WHEN** the presenter pastes a copied code block that is a single line
- **THEN** the original command executes followed by `next`, which copies the next block to the clipboard

#### Scenario: Pasting a multiline block
- **WHEN** the presenter pastes a copied code block that spans multiple lines
- **THEN** all lines of the original command execute, then `next` runs, copying the next block to the clipboard

#### Scenario: Pasting the last block in a step
- **WHEN** the presenter pastes the last code block in a step
- **THEN** the command executes, `next` runs, and a "no more blocks" message is displayed
