#!/usr/bin/env bash

remoteInit() {
  wexampleSiteLoadVariables

  while true;do
    # Test connexion to prod.
    if [ "${PROD_SSH_USER}" != "" ] &&
       [ "${PROD_SSH_HOST}" != "" ] &&
       [ "${PROD_SSH_PRIVATE_KEY}" != "" ] &&
       [ $(wex ssh/check -u=${PROD_SSH_USER} -host=${PROD_SSH_HOST} -k=${PROD_SSH_PRIVATE_KEY}) == true ];then
      # Great.
      return
    else
      if [ "${PROD_SSH_USER}" != "" ];then
        echo "Unable to connect "${SSH_USER}"@"${SSH_HOST}
      fi

      wex var/localClear -n="PROD_SSH_USER" -s
      local SSH_USER=$(wex var/localGet -r -s -n="PROD_SSH_USER" -a="Production username" -d="$(whoami)")

      wex var/localClear -n="PROD_SSH_HOST" -s
      local SSH_HOST=$(wex var/localGet -r -s -n="PROD_SSH_HOST" -a="Production host")

      wex var/localClear -n="PROD_SSH_PORT" -s
      local SSH_PORT=$(wex var/localGet -r -s -n="PROD_SSH_PORT" -a="Production port" -d="22")

      wex var/localClear -n="PROD_SSH_PRIVATE_KEY" -s
      local SSH_PRIVATE_KEY=$(wex ssh/keySelect -n="PROD_SSH_PRIVATE_KEY" -a="SSH Private key path")
    fi
  done;
}
