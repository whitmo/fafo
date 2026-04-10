#!/usr/bin/env bash
# shellcheck shell=bash
# showoff split-pane viewer — runs in the left pane
# Renders step list with active step expanded, polls for changes
set -euo pipefail

# Required env vars
: "${SHOWOFF_STEPS_DIR:?SHOWOFF_STEPS_DIR must be set}"
: "${SHOWOFF_WORKSPACE:?SHOWOFF_WORKSPACE must be set}"

STATE_FILE="$SHOWOFF_WORKSPACE/.showoff-state"
ACTIVE_STEP_FILE="$SHOWOFF_WORKSPACE/.showoff-active-step"
BLOCK_INDEX_FILE="$SHOWOFF_WORKSPACE/.showoff-block-index"
PID_FILE="$SHOWOFF_WORKSPACE/.showoff-viewer-pid"

# Store viewer PID for crash detection
echo $$ > "$PID_FILE"
trap 'rm -f "$PID_FILE"' EXIT

# --- Helpers ---

get_title() {
  head -20 "$1" | grep -m1 '^# ' | sed 's/^# //'
}

is_complete() {
  [[ -f "$STATE_FILE" ]] && grep -qxF "$1" "$STATE_FILE"
}

get_active_step() {
  if [[ -f "$ACTIVE_STEP_FILE" ]]; then
    cat "$ACTIVE_STEP_FILE"
  fi
}

get_block_index() {
  if [[ -f "$BLOCK_INDEX_FILE" ]]; then
    cat "$BLOCK_INDEX_FILE"
  else
    echo "0"
  fi
}

# Count shell code blocks in a file (skip viz blocks)
count_blocks() {
  local file="$1"
  local count=0
  local in_block=false
  local is_viz=false
  while IFS= read -r line; do
    if [[ "$in_block" == false ]]; then
      if [[ "$line" == '```viz' ]]; then
        in_block=true
        is_viz=true
      elif [[ "$line" == '```sh' ]] || [[ "$line" == '```bash' ]] || [[ "$line" == '```shell' ]] || [[ "$line" == '```' ]]; then
        in_block=true
        is_viz=false
      fi
    else
      if [[ "$line" == '```' ]]; then
        in_block=false
        if [[ "$is_viz" == false ]]; then
          count=$((count + 1))
        fi
      fi
    fi
  done < "$file"
  echo "$count"
}

# --- Block highlighting pre-processor ---
# Takes a markdown file and block index, outputs modified markdown with
# current block highlighted and completed/upcoming blocks dimmed.
preprocess_blocks() {
  local file="$1"
  local current_idx="$2"
  local block_num=0
  local in_block=false
  local is_viz=false

  local viz_cmd=""

  while IFS= read -r line; do
    if [[ "$in_block" == false ]]; then
      if [[ "$line" == '```viz' ]]; then
        in_block=true
        is_viz=true
        viz_cmd=""
      elif [[ "$line" == '```sh' ]] || [[ "$line" == '```bash' ]] || [[ "$line" == '```shell' ]] || [[ "$line" == '```' ]]; then
        in_block=true
        is_viz=false
        if [[ $block_num -eq $current_idx ]]; then
          # Current block — wrap in blockquote for glow highlighting
          echo "> $line"
        else
          echo "$line"
        fi
      else
        echo "$line"
      fi
    else
      if [[ "$line" == '```' ]]; then
        in_block=false
        if [[ "$is_viz" == true ]]; then
          # Execute viz command, show output inline
          local viz_tool
          viz_tool=$(echo "$viz_cmd" | awk '{print $1}')
          if command -v "$viz_tool" &>/dev/null; then
            eval "$viz_cmd" 2>/dev/null || echo "$viz_cmd"
          else
            echo "$viz_cmd"
            echo "*($viz_tool not installed)*"
          fi
          echo ""
        else
          if [[ $block_num -eq $current_idx ]]; then
            echo "> $line"
          else
            echo "$line"
          fi
          block_num=$((block_num + 1))
        fi
      else
        if [[ "$is_viz" == true ]]; then
          if [[ -n "$viz_cmd" ]]; then
            viz_cmd="$viz_cmd"$'\n'"$line"
          else
            viz_cmd="$line"
          fi
        elif [[ $block_num -eq $current_idx ]]; then
          echo "> $line"
        else
          echo "$line"
        fi
      fi
    fi
  done < "$file"
}

# --- Render ---

render() {
  clear

  local active_step
  active_step=$(get_active_step)
  local block_idx
  block_idx=$(get_block_index)

  local step_num=0
  local total_steps=0
  local active_step_num=0

  # Count total steps
  for f in "$SHOWOFF_STEPS_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    total_steps=$((total_steps + 1))
  done

  echo ""

  # Render each step
  for f in "$SHOWOFF_STEPS_DIR"/*.md; do
    [[ -f "$f" ]] || continue
    step_num=$((step_num + 1))
    local filename
    filename=$(basename "$f")
    local title
    title=$(get_title "$f")
    local num="${filename%%[-_]*}"

    if [[ "$filename" == "$active_step" ]]; then
      # Active step — expanded
      active_step_num=$step_num
      printf '\033[1;33m▶ %s - %s\033[0m\n' "$num" "$title"
      echo ""

      # Render markdown with block highlighting
      if command -v glow &>/dev/null; then
        preprocess_blocks "$f" "$block_idx" | glow -w "$(tput cols)" - 2>/dev/null || cat "$f"
      else
        preprocess_blocks "$f" "$block_idx"
      fi
      echo ""
    elif is_complete "$filename"; then
      printf '\033[2m✓ %s - %s\033[0m\n' "$num" "$title"
    else
      printf '○ %s - %s\n' "$num" "$title"
    fi
  done

  # Step/block counter
  if [[ -n "$active_step" ]] && [[ -f "$SHOWOFF_STEPS_DIR/$active_step" ]]; then
    local total_blocks
    total_blocks=$(count_blocks "$SHOWOFF_STEPS_DIR/$active_step")
    echo ""
    printf '\033[2mStep %s/%s | Block %s/%s\033[0m\n' \
      "$active_step_num" "$total_steps" "$block_idx" "$total_blocks"
  fi
}

# --- Main loop: poll for changes, re-render on change ---

last_active=""
last_index=""
last_state=""

# Initial render
render

while true; do
  sleep 0.5

  cur_active=$(get_active_step)
  cur_index=$(get_block_index)
  cur_state=""
  [[ -f "$STATE_FILE" ]] && cur_state=$(cat "$STATE_FILE")

  # Only re-render if something changed (implicit debounce)
  if [[ "$cur_active" != "$last_active" ]] || \
     [[ "$cur_index" != "$last_index" ]] || \
     [[ "$cur_state" != "$last_state" ]]; then
    render
    last_active="$cur_active"
    last_index="$cur_index"
    last_state="$cur_state"
  fi
done
