#!/usr/bin/env bash

siteDeployArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
    [1]='upwex upwex "Use last version of wexample scripts (debug mode)" false'
  )
}

siteDeploy() {

  if [ "${UPWEX+x}" == true ]; then

    # Save current dir.
    CURRENT_DIR=$(realpath ./)

    # Reinstall wexample from github.
    rm -rf /opt/wexample
    cd /opt/
    mkdir wexample
    cd wexample
    git clone https://github.com/wexample/scripts.git .
    . project/bash/default/_installLocal.sh

    UPWEX=false
    # Go back to project.
    cd ${CURRENT_DIR}
    # Relaunch with debug mode.
    wex site/deploy --debug

    return
  fi;

  . .wex

  wex ci/exec -c=deploy

  # There is a production site configured in .wex.
  if [ "${PROD_SSH_HOST}" != "" ]; then
    # Check gitlab credentials and init.
    wex wexample::gitlab/sshInit
    # Update on production server
    # Create gitlab user :
    #   adduser gitlab
    #   usermod -aG sudo gitlab
    #   mkdir /home/gitlab/.ssh/
    # Public key ~/.ssh/id_rsa of gitlab server must be added on production server.
    #   nano /home/gitlab/.ssh/authorized_keys
    # User must have access to execute scripts.
    # Use : sudo visudo
    # then add : username ALL=(ALL) NOPASSWD: ALL
    # If root ssh access is disabled.
    wex wexample::remote/exec -e=prod -h="${PROD_SSH_HOST}" -u=gitlab -k=/deployKey -d=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SITE_NAME} -s="wex site/pull"
  fi;
}
