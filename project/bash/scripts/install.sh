#!/usr/bin/env bash

scriptsInstallArgs() {
  _AS_NON_SUDO=false
  _DESCRIPTION='Install all scripts requirements'
  _ARGUMENTS=(
    'dir d "Directory (inside bash)" true'
  )
}

scriptsInstall() {
  local REQUIREMENTS
  REQUIREMENTS=("$(wex scripts/requirements -d="${DIR}")")

  if [ "${REQUIREMENTS[@]}" != "" ];then
    apt-get update && apt-get install -yq ${REQUIREMENTS[@]}
  fi;
}
