#!/usr/bin/env bash

gitHasChangeArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='Return true if there is a change in the current directory.'
}

gitHasChange() {
  local -r gitStatus="$(git status --porcelain)"
  if [[ -n "$gitStatus" ]]; then
    echo true
    return
  fi

  local -r gitDiff="$(git diff)"
  if [[ -n "$gitDiff" ]]; then
    echo true
    return
  fi

  echo false
}
