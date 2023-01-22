#!/usr/bin/env bash

scriptsRequirementsArgs() {
  _DESCRIPTION='Returns all the requirements for scripts directory'
  _ARGUMENTS=(
    'dir d "Directory of scripts" true'
  )
}

scriptsRequirements() {
  local SCRIPTS
  local OUTPUT
  SCRIPTS=$(wex scripts/list -d="${DIR}")

  for SCRIPT in ${SCRIPTS[@]}
  do
    local ARRAY
    ARRAY=$(wex script/requirements -s="${SCRIPT}")
    ARRAY=$(wex array/join -a="${ARRAY}")

    if [ -n "${ARRAY}" ];then
      OUTPUT+="${ARRAY} "
    fi
  done

  echo "${OUTPUT}"
}
