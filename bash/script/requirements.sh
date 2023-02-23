#!/usr/bin/env bash

scriptRequirementsArgs() {
  _DESCRIPTION='Returns requirements for giver script name'
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'script s "Full name of script" true'
  )
}

scriptRequirements() {
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
    local _REQUIREMENTS

    # Load
    ${METHOD}

    # Avoid empty values
    if [ ! -z "${_REQUIREMENTS+x}" ];then
      echo ${_REQUIREMENTS[@]}
    fi;
  fi
}
