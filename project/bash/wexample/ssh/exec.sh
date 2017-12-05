#!/usr/bin/env bash

sshExecArgs() {
 _ARGUMENTS=(
   [0]='username u "SSH Username" true'
   [1]='shell_script s "Command to execute from shell, relative to site directory" true'
   [2]='dir_site d "Local root site directory" false'
 )
}

sshExec() {
  # Use current dir by default
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  wex wexample::site/deployCredentials -d=${DIR_SITE}

  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  COMMAND='cd '${DEPLOY_PATH_ROOT}' && sudo bash '${WEX_LOCAL_DIR}'project/bash/ubuntu-16.x/_exec.sh "'${SHELL_SCRIPT}'"'

  ssh -t -p${DEPLOY_PORT} ${USERNAME}@${DEPLOY_IPV4} ${COMMAND}
}
