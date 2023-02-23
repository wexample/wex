#!/usr/bin/env bash

scriptsInstallArgs() {
  _AS_NON_SUDO=false
  # shellcheck disable=SC2034
  _DESCRIPTION='Install all scripts requirements'
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'dir d "Directory (inside bash)" true'
  )
}

scriptsInstall() {
  local REQUIREMENTS
  REQUIREMENTS=("$(wex-exec scripts/requirements -d="${DIR}")")

  if [ "${REQUIREMENTS[@]}" != "" ];then
    apt-get update && apt-get install -yq ${REQUIREMENTS[@]}
  fi;
}
