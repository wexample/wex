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

  # Conf contains site name
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployIpv4);
  DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployPort);
  DEPLOY_USER=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployUser);
  PROD_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=prodPathRoot);

  # Update on production server
  # User must have access to execute scripts.
  # Use : sudo visudo
  # then add : username ALL=(ALL) NOPASSWD: ALL
  # If root ssh access is disabled.
  ssh -t -p${DEPLOY_PORT} ${DEPLOY_USER}@${DEPLOY_IPV4} "cd ${PROD_PATH_ROOT} && sudo bash wexample/update.sh"
}
