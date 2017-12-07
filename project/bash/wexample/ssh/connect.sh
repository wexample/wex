#!/usr/bin/env bash

sshConnectArgs() {
  _ARGUMENTS=(
    [0]='ssh_username u "SSH Username" false'
    [1]='ssh_private_key pk "SSH Private key" false'
    [2]='environment e "Environment to connect to" true'
  )
}

sshConnect() {
  wex env/credentials -e=${ENVIRONMENT} -u=${SSH_USERNAME} -pk=${SSH_PRIVATE_KEY}
  ssh-keygen -R ${SITE_IPV4}
  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  ssh -oStrictHostKeyChecking=no -i${SITE_PRIVATE_KEY} -p${SITE_PORT} ${SITE_USERNAME}@${SITE_IPV4}
  # Prevent to set credentials globally
  wex env/credentialsClear
}
