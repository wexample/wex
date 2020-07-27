#!/usr/bin/env bash

appExecArgs() {
  _DESCRIPTION="Execute a script from inside the container, at project root"
  _ARGUMENTS=(
    'command c "Bash command to execute" true'
  )
}

appExec() {
  # TODO Use v2 script, localized.
  wex site/exec -l -c="${COMMAND}"
}