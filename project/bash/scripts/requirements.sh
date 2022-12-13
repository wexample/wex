#!/usr/bin/env bash

scriptsRequirementsArgs() {
  _DESCRIPTION='Returns all the requirements for scripts directory'
  _ARGUMENTS=(
    'dir d "Directory of scripts" true'
  )
}

scriptsRequirements() {
  local SCRIPTS
  SCRIPTS=$(wex scripts/list -d="${DIR}")

  for SCRIPT in ${SCRIPTS[@]}
  do
    wex script/requirements -s="${SCRIPT}"
  done
}
