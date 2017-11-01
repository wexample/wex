#!/usr/bin/env bash

wexampleSiteDeployArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
  )
}

wexampleSiteDeploy() {
  if [ -z "${STAGING_PRIVATE_KEY+x}" ]; then
    echo "Missing private key file"
    exit 1
  fi;

  # Use current dir by default
  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  # Init using wexample"s gitlab specific configuration.
  wex wexample/gitlabSshInit

  # Update on production server
  # User must have access to execute scripts.
  # Use : sudo visudo
  # then add : username ALL=(ALL) NOPASSWD: ALL
  # If root ssh access is disabled.
  wex wexample/siteSshExec -d=${DIR} -s="wexample/update.sh"
}
