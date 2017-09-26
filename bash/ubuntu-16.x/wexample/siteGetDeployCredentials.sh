#!/usr/bin/env bash

wexampleSiteGetDeployCredentialsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Local root site directory" true'
  )
}

wexampleSiteGetDeployCredentials() {
  # Conf contains site name
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);
  DEPLOY_IPV4=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployIpv4);
  DEPLOY_PORT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployPort);
  DEPLOY_USER=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=deployUser);
  PROD_PATH_ROOT=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=prodPathRoot);
}
