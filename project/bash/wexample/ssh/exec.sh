#!/usr/bin/env bash

sshExecArgs() {
  _ARGUMENTS=(
    [0]='ssh_username u "SSH Username" false'
    [1]='ssh_private_key pk "SSH Private key" false'
    [2]='environment e "Environment to connect to" true'
    [3]='shell_script s "Command to execute from shell, relative to site directory" true'
  )
}

sshExec() {
  wex env/credentials -e=${ENVIRONMENT} -u=${SSH_USERNAME} -pk=${SSH_PRIVATE_KEY}
  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  echo COMMAND='cd '${SITE_PATH_ROOT}' && sudo bash '${WEX_LOCAL_DIR}'project/bash/ubuntu-16.x/_exec.sh "'${SHELL_SCRIPT}'"'
  COMMAND='cd '${SITE_PATH_ROOT}' && sudo bash '${WEX_LOCAL_DIR}'project/bash/ubuntu-16.x/_exec.sh "'${SHELL_SCRIPT}'"'
  ssh -oLogLevel=QUIET -i${SITE_PRIVATE_KEY} -t -p${SITE_PORT} ${SITE_USERNAME}@${SITE_IPV4} ${COMMAND}
  # Prevent to set credentials globally
  wex env/credentialsClear
}
