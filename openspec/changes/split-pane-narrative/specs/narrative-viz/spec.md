## ADDED Requirements

### Requirement: Viz code blocks in step markdown
Step markdown files SHALL support fenced code blocks tagged `viz` that the viewer executes and renders inline.

#### Scenario: Sparkline viz block
- **WHEN** a step markdown contains a `viz` block with `spark 0 30 55 80 33 150`
- **THEN** the viewer executes the command and displays the sparkline output (`▁▂▃▅▂▇`) in place of the code block

#### Scenario: Viz blocks are not copied to clipboard
- **WHEN** the `next` command parses code blocks in a step
- **THEN** blocks tagged `viz` are skipped — only `sh`, `bash`, `shell`, and untagged blocks are copied to clipboard

### Requirement: Graceful viz fallback
The viewer SHALL handle missing viz dependencies gracefully.

#### Scenario: Viz command not found
- **WHEN** a `viz` block references a command that is not installed (e.g., `spark` or `plotext`)
- **THEN** the viewer displays the raw command text instead of executing it, with a note indicating the tool is not available
