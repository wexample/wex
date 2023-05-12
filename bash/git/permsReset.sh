#!/usr/bin/env bash

gitPermsResetArgs() {
  _DESCRIPTION='Revert permissions changes on folder'
  _ARGUMENTS=(
  )
}

gitPermsReset() {
  diff=$(git diff -p -R --no-color | grep -E "^(diff|(old|new) mode)" --color=never)
  # Avoid error if empty.
  [ -z "$diff" ] || echo "$diff" | git apply
}
