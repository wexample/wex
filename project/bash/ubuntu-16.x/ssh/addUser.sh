#!/usr/bin/env bash

sshAddUserArgs() {
  _ARGUMENTS=(
    [0]='user_ssh u "User" true'
    [1]='group g "Group" false'
    [2]='key k "SSH Key to use" true'
  )
}

sshAddUser() {
  if [ "${GROUP}" == "" ];then
    local GROUP=${USER_SSH}
  fi

  # Create SSH dir.
  local SSH_DIR=/home/${USER_SSH}/.ssh
  mkdir -p ${SSH_DIR}
  chown ${USER_SSH}:${GROUP} ${SSH_DIR}
  chmod 700 ${SSH_DIR}

  # Add wexample SSH key
  local AUTH_KEYS=${SSH_DIR}/authorized_keys
  touch ${AUTH_KEYS}
  wex file/textAppend -f=${AUTH_KEYS} -l="${KEY}"

  chown ${USER_SSH}:${GROUP} ${AUTH_KEYS}
  chmod 600 ${AUTH_KEYS}
}
