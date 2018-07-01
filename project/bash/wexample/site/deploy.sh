#!/usr/bin/env bash

siteDeployArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of site" false'
    [1]='upwex upwex "Use last version of wexample scripts (debug mode)" false'
    [2]='deploy_env e "Deployment env" true'
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
    . project/bash/default/_installLocal.sh --depth=1

    UPWEX=false
    # Go back to project.
    cd ${CURRENT_DIR}
    # Relaunch with debug mode.
    wex site/deploy -e=${DEPLOY_ENV}

    return
  fi;

  . .wex

  wex ci/exec -c=deploy

  local SSH_HOST=$(eval 'echo ${'${DEPLOY_ENV}'_SSH_HOST}')

  # There is a site configured in .wex for this env.
  if [ "${SSH_HOST}" != "" ]; then

    # Set GIT user.
    git config --global user.email "deploy@pipeline.com"
    git config --global user.name "Deploy"

    # Check gitlab credentials and init.
    wex wexample::gitlab/sshInit
    # Update on destination server
    # Create gitlab user :
    #   adduser gitlab
    #   usermod -aG sudo gitlab
    #   mkdir /home/gitlab/.ssh/
    # Public key ~/.ssh/id_rsa of gitlab server must be added on destination server.
    #   nano /home/gitlab/.ssh/authorized_keys
    # User must have access to execute scripts.
    # Use : sudo visudo
    # then add : username ALL=(ALL) NOPASSWD: ALL
    # If root ssh access is disabled.
    local ARGS="-e=${DEPLOY_ENV} -h="${PROD_SSH_HOST}" -u=gitlab -k=/root/.ssh/host/id_rsa"
    # Print login info for easiest debug.
    echo "Connecting to : ssh "$(wex wexample::remote/connexion ${ARGS})
    # Connect && exec.
    wex wexample::remote/exec ${ARGS} -d=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${NAME} -s="sudo wex site/pull"
  fi;
}
