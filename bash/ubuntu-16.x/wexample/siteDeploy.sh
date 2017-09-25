#!/usr/bin/env bash

wexampleSiteDeploy() {
  if [ -z "${STAGING_PRIVATE_KEY+x}" ]; then
    echo "Missing private key file"
    exit 1
  fi;

  # ${STAGING_PRIVATE_KEY} must be registered into project variables.
  wex gitlab/sshInit -k=${STAGING_PRIVATE_KEY}

  FILE_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=containerPathRoot);
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployIpv4);
  DEPLOY_USER=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployUser);

  # Update on production server
  # User must have access to execute scripts.
  # Use : sudo visudo
  # then add : username ALL=(ALL) NOPASSWD: ALL
  # If root ssh access is disabled.
  ssh -t -p54345 ${DEPLOY_USER}@${DEPLOY_IPV4} "sudo bash ${FILE_PATH_ROOT}wexample/update.sh"
}
