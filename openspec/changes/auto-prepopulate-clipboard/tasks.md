## 1. Modify `next` to append `; next` to clipboard

- [x] 1.1 Update `_showoff_copy` calls in the `next` function to append `; next` to the clipboard content
- [x] 1.2 Verify multiline blocks paste correctly with `; next` on the last line

## 2. Auto-copy first block on shell init

- [x] 2.1 Add auto-copy of first block at end of `_shell-init.sh` init sequence (after welcome message)
- [x] 2.2 Handle edge case where step has zero code blocks (skip clipboard, show message)

## 3. Verify

- [ ] 3.1 Run `make demo` and walk through a step — confirm clipboard is pre-loaded on entry
- [ ] 3.2 Paste and execute — confirm next block auto-loads into clipboard
- [ ] 3.3 Confirm last block prints "no more blocks" after `; next` runs
- [x] 3.4 Run shellcheck on modified `_shell-init.sh`
