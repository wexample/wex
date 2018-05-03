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

  . .wex

  wex ci/exec -c=deploy

  # There is a production site configured in .wex.
  if [ "${PROD_SSH_HOST}" != "" ]; then
    # Check gitlab credentials and init.
    wex wexample::gitlab/sshInit
    # TODO Still valid ?
    # Update on production server
    # User must have access to execute scripts.
    # Use : sudo visudo
    # then add : username ALL=(ALL) NOPASSWD: ALL
    # If root ssh access is disabled.
    wex wexample::remote/exec -e=prod -h="${PROD_SSH_HOST}" -u=gitlab -pk=/deployKey -d=${DIR} -s="wex wexample::site/pull"
  fi;
}
