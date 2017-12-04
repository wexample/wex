#!/usr/bin/env bash

siteDeployCredentialsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Local root site directory" true'
  )
}

siteDeployCredentials() {
  # Conf contains site name
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wex.json -k=siteName);
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wex.json -k=deployIpv4);
  DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR}wex.json -k=deployPort);
  DEPLOY_USER=$(wex file/jsonReadValue -f=${DIR}wex.json -k=deployUser);
  PROD_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wex.json -k=prodPathRoot);
}
