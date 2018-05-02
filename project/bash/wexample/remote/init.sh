#!/usr/bin/env bash

remoteInit() {
  wexampleSiteInitLocalVariables
  . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

  while true;do

      # Test connexion to prod.
      if [ "${PROD_SSH_USER}" != "" ] &&
         [ "${PROD_SSH_HOST}" != "" ] &&
         [ "${PROD_SSH_PRIVATE_KEY}" != "" ];then
         if [ "$(wex ssh/check -u=${PROD_SSH_USER} -p=${PROD_SSH_PORT} -h=${PROD_SSH_HOST} -k=${PROD_SSH_PRIVATE_KEY})" == true ];then
           # Great.
           return
         fi
         echo "Unable to connect "${PROD_SSH_USER}"@"${PROD_SSH_HOST}:${PROD_SSH_PORT}" using "${PROD_SSH_PRIVATE_KEY}
      fi

      PROD_SSH_USER=''
      wex var/localClear -n="PROD_SSH_USER"
      local PROD_SSH_USER=$(wex var/localGet -r -s -n="PROD_SSH_USER" -a="Production username")

      PROD_SSH_HOST=''
      wex var/localClear -n="PROD_SSH_HOST"
      local PROD_SSH_HOST=$(wex var/localGet -r -s -n="PROD_SSH_HOST" -a="Production host")

      PROD_SSH_PORT=''
      wex var/localClear -n="PROD_SSH_PORT"
      local PROD_SSH_PORT=$(wex var/localGet -r -s -n="PROD_SSH_PORT" -a="Production SSH port")

      PROD_SSH_PRIVATE_KEY=''
      wex var/localClear -n="PROD_SSH_PRIVATE_KEY"
      # Get value.
      local PROD_SSH_PRIVATE_KEY=$(wex var/localGet -r -s -n="PROD_SSH_PRIVATE_KEY" -d="")
      if [ "${PROD_SSH_PRIVATE_KEY}" == "" ];then
        wex ssh/keySelect -n="PROD_SSH_PRIVATE_KEY" -d="SSH Private key for production environment"
        local PROD_SSH_PRIVATE_KEY=$(wex var/localGet -r -s -n="PROD_SSH_PRIVATE_KEY")
      fi
  done;
}
