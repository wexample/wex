#!/usr/bin/env bash

siteDeployCredentialsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Local root site directory" true'
  )
}

siteDeployCredentials() {
  # Conf contains site name
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wex.json -k=name);
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wex.json -k=prod.ipv4);
  DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR}wex.json -k=prod.port);
  DEPLOY_USER=gitlab
  DEPLOY_PATH_ROOT=/var/www/${SITE_NAME}
}
