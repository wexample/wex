#!/usr/bin/env bash

remoteInit() {
  _ARGUMENTS=(
    [0]='recreate r "Restart publishing configuration" true'
    [1]='env e "Environment to initialize" true'
  )
}

remoteInit() {
  # Recreate ?
  if [ "${RECREATE}" != true ];then
    wexampleSiteInitLocalVariables
    . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}
    local SSH_USER=$(eval 'echo ${'${ENV}'_SSH_USER}')
    local SSH_HOST=$(eval 'echo ${'${ENV}'_SSH_HOST}')
    local SSH_PORT=$(eval 'echo ${'${ENV}'_SSH_PORT}')
    local SSH_PRIVATE_KEY=$(eval 'echo ${'${ENV}'_SSH_PRIVATE_KEY}')
  fi

  local ENV=${ENV^^}

  while true;do
      # Test connexion to prod.
      if [ "${SSH_USER}" != "" ] &&
         [ "${SSH_HOST}" != "" ] &&
         [ "${SSH_PRIVATE_KEY}" != "" ];then
         wex ssh/check -u=${SSH_USER} -p=${SSH_PORT} -h=${SSH_HOST} -k=${SSH_PRIVATE_KEY}
         if [ "$(wex ssh/check -u=${SSH_USER} -p=${SSH_PORT} -h=${SSH_HOST} -k=${SSH_PRIVATE_KEY})" == true ];then
           # Great.
           return
         fi
         echo "Unable to connect "${SSH_USER}"@"${SSH_HOST}:${SSH_PORT}" using "${SSH_PRIVATE_KEY}
      fi

      SSH_USER=''
      wex var/localClear -n="${ENV}_SSH_USER"
      local SSH_USER=$(wex var/localGet -r -s -n="${ENV}_SSH_USER" -a="Server login username")

      SSH_HOST=''
      wex var/localClear -n="${ENV}_SSH_HOST"
      local SSH_HOST=$(wex var/localGet -r -s -n="${ENV}_SSH_HOST" -a="Server host")

      SSH_PORT=''
      wex var/localClear -n="${ENV}_SSH_PORT"
      local SSH_PORT=$(wex var/localGet -r -s -n="${ENV}_SSH_PORT" -a="Server SSH port")

      SSH_PRIVATE_KEY=''
      wex var/localClear -n="${ENV}_SSH_PRIVATE_KEY"
      # Get value.
      local SSH_PRIVATE_KEY=$(wex var/localGet -r -s -n="${ENV}_SSH_PRIVATE_KEY" -d="")
      if [ "${SSH_PRIVATE_KEY}" == "" ];then
        wex ssh/keySelectList
        wex ssh/keySelect -n="${ENV}_SSH_PRIVATE_KEY" -d="SSH Private key for server"
        local SSH_PRIVATE_KEY=$(wex var/localGet -r -s -n="${ENV}_SSH_PRIVATE_KEY")
      fi
  done;
}
