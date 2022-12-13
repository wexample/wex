#!/usr/bin/env bash

scriptArgumentsArgs() {
  _DESCRIPTION='Returns requirements for giver script name'
  _ARGUMENTS=(
    'script s "Full name of script" true'
  )
}

scriptArguments() {
  local METHOD

  METHOD=$(_wexMethodNameArgs "${SCRIPT}")
  FILE=$(_wexFindScriptFile "${SCRIPT}")

  # File not found.
  if [ ! -f "${FILE}" ]; then
    return
  fi

  # Load
  . "${FILE}"

  if [ "$(type -t "${METHOD}")" = "function" ];then
    local _ARGUMENTS

    # Load
    ${METHOD}

    printf '%s\n' "${_ARGUMENTS[@]}"
  fi
}
