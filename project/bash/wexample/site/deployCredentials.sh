#!/usr/bin/env bash

siteDeployCredentialsArgs() {
  _ARGUMENTS=(
    [0]='dir_site d "Local root site directory" false'
  )
}

siteDeployCredentials() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Conf contains site name
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR_SITE}wex.json -k=name);
  # TODO variable env
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR_SITE}wex.json -k=prod.ipv4);
  DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR_SITE}wex.json -k=prod.port);
  DEPLOY_PATH_ROOT=/var/www/${SITE_NAME}
}
