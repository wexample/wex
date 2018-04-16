#!/usr/bin/env bash

sshKeySelectArgs() {
  _ARGUMENTS=(
    [0]='name n "SSH Key local name" true'
    [1]='description d "Description" true'
  )
}

sshKeySelect() {
  # Find local key.
  local RSA_PATH=~/.ssh/

  local SSH_PRIVATE_KEY=''
  while [ "${SSH_PRIVATE_KEY}" == "" ];do
    # Get SSH get
    SSH_PRIVATE_KEY=$(wex wexample::var/localGet -n="${NAME}" -a="${DESCRIPTION}" -s -r)

    if [ ! -f ${SSH_PRIVATE_KEY} ];then
      # Ask again.
      SSH_PRIVATE_KEY=''
    fi
  done

  echo ${SSH_PRIVATE_KEY}
}
