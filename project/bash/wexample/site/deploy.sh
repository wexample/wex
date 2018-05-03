#!/usr/bin/env bash

siteDeployArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
    [1]='upwex upwex "Use last version of wexample scripts (debug mode)" false'
  )
}

siteDeploy() {

  if [ ! -z "${UPWEX+x}" ]; then

    # Save current dir.
    CURRENT_DIR=$(realpath ./)

    # Reinstall wexample from github.
    rm -rf /opt/wexample
    cd /opt/
    mkdir wexample
    cd wexample
    git clone https://github.com/wexample/scripts.git .
    . project/bash/default/_installLocal.sh

    # Go back to project.
    cd ${CURRENT_DIR}
    # Relaunch with debug mode.
    wex site/deploy --debug

    return
  fi;

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
    # Update on production server
    # User must have access to execute scripts.
    # Use : sudo visudo
    # then add : username ALL=(ALL) NOPASSWD: ALL
    # If root ssh access is disabled.
    wex wexample::remote/exec -e=prod -h="${PROD_SSH_HOST}" -u=gitlab -pk=/deployKey -d=${DIR} -s="wex wexample::site/pull"
  fi;
}
