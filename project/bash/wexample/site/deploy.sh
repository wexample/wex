#!/usr/bin/env bash

siteDeployArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
  )
}

siteDeploy() {
  # Use current dir by default
  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  local PROD_IPV4=$(wex json/readValue -f=wex.json -k=prod.ipv4)

  wex ci/exec -c=deploy

  # There is a production site configured in wex.json.
  if [ "${PROD_IPV4}" != "" ]; then
    # Check gitlab credentials and init.
    wex wexample::gitlab/sshInit
    # Update on production server
    # User must have access to execute scripts.
    # Use : sudo visudo
    # then add : username ALL=(ALL) NOPASSWD: ALL
    # If root ssh access is disabled.
    wex wexample::ssh/exec -u=gitlab -pk=/deployKey -d=${DIR} -e=prod -s="wex wexample::site/pull"
  fi;
}
