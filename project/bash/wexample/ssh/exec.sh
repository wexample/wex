#!/usr/bin/env bash

sshExecArgs() {
 _ARGUMENTS=(
   [0]='dir d "Local root site directory" true'
   [1]='shell_script s "Command to execute from shell, relative to site directory" true'
 )
}

sshExec() {
  wex wexample::site/deployCredentials -d=${DIR}

  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  COMMAND='cd ${DEPLOY_PATH_ROOT} && sudo bash ${WEX_DIR_BASH_DEFAULT}_exec.sh "${SHELL_SCRIPT}"'

  ssh -t -p${DEPLOY_PORT} ${DEPLOY_USER}@${DEPLOY_IPV4} ${COMMAND}
}
