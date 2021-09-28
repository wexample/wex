#!/usr/bin/env bash

remoteGoArgs() {
  _DESCRIPTION="SSH connect to remote environment"
  _ARGUMENTS=(
    'env e "Remote environment name" false'
  )
}

remoteGo() {
  . .wex
  . .env

  _wexMessage "Your are switching environment to ${ENV^^}."

  local REMOTE_HOST=$(wex env/getVar -n=SERVER_MAIN -e="${ENV}")
  local REMOTE_USERNAME=$(wex remote/getSshUsername)

  ssh ${REMOTE_USERNAME}@${REMOTE_HOST}

  . .env
  _wexMessage "Your have switched back environment to ${SITE_ENV^^}."
}