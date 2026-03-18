# showoff

A bash+gum demo runner. Write step-by-step demos as markdown, present them interactively in the terminal.

## Install

```sh
brew install gum
```

Optional (for split-pane mode): `brew install tmux`
Optional (for markdown rendering in split-pane): `brew install glow`

## Quick start

```sh
# Run a demo
./bin/showoff ./path/to/steps ./workspace

# Split-pane mode (narrative left, shell right)
./bin/showoff --split ./path/to/steps ./workspace

# Reset completion state
./bin/showoff --reset ./path/to/steps ./workspace
```

## Writing step files

Create numbered markdown files in a steps directory:

```
my-demo/steps/
  01-setup.md
  02-build.md
  03-deploy.md
  cleanup.md
```

Each file is one step. The filename determines sort order. The first `# Heading` is the step title shown in the list.

### Step format

````markdown
# Step Title

Narrative text explaining what we're about to do.

```sh
echo "this block gets copied to clipboard"
```

More narrative. The audience sees this context.

```sh
curl -s https://api.example.com/health | jq .
```
````

**Code blocks** tagged `sh`, `bash`, `shell`, or untagged are copied to clipboard by `next`.

**Viz blocks** (split-pane only) execute in the viewer pane and render inline:

````markdown
```viz
spark 0 30 55 80 33 150
```
````

### Presenter flow

1. Select a step from the list
2. First code block is auto-copied to clipboard and pre-filled in the prompt
3. Paste and run — `; next` is appended, which auto-loads the next block
4. Repeat until all blocks are done
5. Type `exit` to return to the step list

### Shell commands

| Command | What it does |
|---------|-------------|
| `next`  | Copy next code block to clipboard, print it |
| `peek`  | Preview next block without advancing |
| `exit`  | Finish step, return to list |

## Split-pane mode

`--split` launches a two-pane tmux layout:

```
+------------------+---------------------------+
| Narrative viewer | Interactive shell         |
| (auto-updates)   |                           |
|                  | [showoff: 01-setup] $ ... |
| Step list with   |                           |
| progress markers |                           |
+------------------+---------------------------+
```

- Left pane shows step list (✓ done, ▶ active, ○ upcoming) with the active step's full markdown expanded
- Current code block is highlighted
- Viewer updates automatically as you run `next`
- If the viewer crashes, the shell continues in single-pane mode
- Requires 100+ columns (140+ recommended)

## Example

See `../litestream/steps/` for a working demo:

```sh
cd ../litestream
../showoff/bin/showoff ./steps ./workspace
```
