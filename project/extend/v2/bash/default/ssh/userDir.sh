#!/usr/bin/env bash

sshUserDirArgs() {
  _ARGUMENTS=(
    [0]='user_ssh u "User" true'
    [1]='create c "Create" false'
  )
}

sshUserDir() {
  # Create SSH dir.
  if [ "${USER_SSH}" == "root" ];then
    local SSH_DIR=/root/.ssh
  else
    local SSH_DIR=/home/${USER_SSH}/.ssh
  fi

  if [ "${CREATE}" == true ];then
    mkdir -p ${SSH_DIR}
    chown ${USER_SSH}:${GROUP} ${SSH_DIR}
    chmod 700 ${SSH_DIR}
  fi

  echo ${SSH_DIR}
}
