#!/usr/bin/env bash

gitHookExecArgs() {
  _ARGUMENTS=(
    [0]='name n "Git hook name" true'
  )
}

# We just append command on git hooks
# We don't check if hooks already exists.
gitHookExec() {
  . ${WEX_DIR_ROOT}"samples/git/hooks/"${NAME}
}
