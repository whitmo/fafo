# shellcheck shell=bash
# showoff shell init — sourced via bash --rcfile
# Provides: next, peek, custom prompt

# Source user's bashrc first for a familiar environment
# shellcheck source=/dev/null
[[ -f ~/.bashrc ]] && source ~/.bashrc 2>/dev/null
# shellcheck source=/dev/null
[[ -f ~/.bash_profile ]] && source ~/.bash_profile 2>/dev/null

# --- Parse code blocks from step markdown ---
_showoff_blocks=()
_showoff_parse_blocks() {
  local file="$1"
  local in_block=false
  local block=""
  while IFS= read -r line; do
    if [[ "$in_block" == false ]]; then
      if [[ "$line" == '```sh' ]] || [[ "$line" == '```bash' ]] || [[ "$line" == '```shell' ]] || [[ "$line" == '```' ]]; then
        in_block=true
        block=""
      fi
    else
      if [[ "$line" == '```' ]]; then
        in_block=false
        _showoff_blocks+=("$block")
      else
        if [[ -n "$block" ]]; then
          block="$block"$'\n'"$line"
        else
          block="$line"
        fi
      fi
    fi
  done < "$file"
}

_showoff_parse_blocks "$SHOWOFF_STEP_FILE"

# --- Block index ---
_showoff_index_file="$SHOWOFF_WORKSPACE/.showoff-block-index"
_showoff_get_index() {
  if [[ -f "$_showoff_index_file" ]]; then
    cat "$_showoff_index_file"
  else
    echo "0"
  fi
}

_showoff_set_index() {
  echo "$1" > "$_showoff_index_file"
}

# --- Clipboard helper ---
_showoff_copy() {
  if command -v pbcopy &>/dev/null; then
    printf '%s' "$1" | pbcopy
  elif command -v xclip &>/dev/null; then
    printf '%s' "$1" | xclip -selection clipboard
  elif command -v xsel &>/dev/null; then
    printf '%s' "$1" | xsel --clipboard --input
  else
    echo "  (no clipboard tool found — copy manually)"
    return 1
  fi
}

# --- Print a code block nicely ---
_showoff_print_block() {
  local block="$1"
  echo ""
  if command -v gum &>/dev/null; then
    echo "$block" | gum style --border rounded --padding "0 1" --border-foreground="99"
  else
    echo "  $block"
  fi
}

# --- next command ---
next() {
  local idx
  idx=$(_showoff_get_index)
  local total=${#_showoff_blocks[@]}

  if [[ $idx -ge $total ]]; then
    echo ""
    echo "No more code blocks in this step. Type 'exit' to continue."
    return 0
  fi

  local block="${_showoff_blocks[$idx]}"
  _showoff_print_block "$block"

  if _showoff_copy "$block"'; next'; then
    echo "  Copied to clipboard — paste to run"
  fi
  echo ""

  _showoff_set_index $((idx + 1))
}

# --- peek command ---
peek() {
  local idx
  idx=$(_showoff_get_index)
  local total=${#_showoff_blocks[@]}

  if [[ $idx -ge $total ]]; then
    echo ""
    echo "No more code blocks in this step."
    return 0
  fi

  local block="${_showoff_blocks[$idx]}"
  _showoff_print_block "$block"
  echo "  (preview — not copied)"
  echo ""
}

# --- Custom prompt ---
PS1="[showoff: $SHOWOFF_STEP_NAME] \w \$ "

# --- Welcome message ---
_showoff_title=$(head -20 "$SHOWOFF_STEP_FILE" | grep -m1 '^# ' | sed 's/^# //')
_showoff_total=${#_showoff_blocks[@]}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  $_showoff_title"
echo "  ${_showoff_total} code block(s) to run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  next  — copy next code block to clipboard"
echo "  peek  — preview next block without advancing"
echo "  exit  — finish this step"
echo ""

# --- Prefill readline buffer (requires bash 4+ for READLINE_LINE) ---
_showoff_prefill_block=""
_showoff_fill_prompt() {
  if [[ -n "$_showoff_prefill_block" ]]; then
    READLINE_LINE="$_showoff_prefill_block"
    READLINE_POINT=${#READLINE_LINE}
    _showoff_prefill_block=""
  fi
}
bind -x '"\e[0n": _showoff_fill_prompt'

# --- Auto-copy first block and prefill prompt ---
if [[ ${#_showoff_blocks[@]} -gt 0 ]]; then
  next
  _showoff_prefill_block="${_showoff_blocks[0]}; next"
  printf '\e[5n'
fi
