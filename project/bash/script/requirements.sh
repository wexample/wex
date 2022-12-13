#!/usr/bin/env bash

scriptRequirementsArgs() {
  _DESCRIPTION='Returns requirements for giver script name'
  _ARGUMENTS=(
    'name n "Full name of script" true'
  )
}

scriptRequirements() {
  local _REQUIREMENTS=()
  local METHOD

  METHOD=$(_wexMethodNameArgs "${NAME}")

  # Load
  . "$(_wexFindScriptFile "${NAME}")"
  # Execute
  ${METHOD}

  echo ${_REQUIREMENTS[@]}
}
