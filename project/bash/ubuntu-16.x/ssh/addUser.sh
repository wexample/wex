#!/usr/bin/env bash

sshAddUserArgs() {
  _ARGUMENTS=(
    [0]='user_ssh u "User" true'
    [1]='group g "Host" true'
    [2]='key k "SSH Key to use" true'
  )
}

sshAddUser() {
  if [ "${GROUP}" == "" ];then
    local GROUP=${USER_SSH}
  fi

  # Create SSH dir.
  mkdir -p /home/${USER_SSH}/.ssh
  chown ${USER_SSH}:${GROUP} /home/${USER_SSH}/.ssh
  chmod 700 /home/${USER_SSH}/.ssh

  # Add wexample SSH key
  wex file/textAppend -f=/home/${USER_SSH}/.ssh/authorized_keys -l="${KEY}"

  chown ${USER_SSH}:${GROUP} /home/${USER_SSH}/.ssh/authorized_keys
  chmod 600 /home/${USER_SSH}/.ssh/authorized_keys
}
