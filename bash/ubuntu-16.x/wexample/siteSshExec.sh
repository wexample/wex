#!/usr/bin/env bash

wexampleSiteSshExecArgs() {
 _ARGUMENTS=(
   [0]='dir d "Local root site directory" true'
   [1]='command c "Command to execute from shell, relative to site directory" true'
 )
}

wexampleSiteSshExec() {
  wex wexample/siteGetDeployCredentials -d=${DIR}
  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  ssh -t -p${DEPLOY_PORT} ${DEPLOY_USER}@${DEPLOY_IPV4} "cd ${PROD_PATH_ROOT} && sudo bash ${WEX_DIR_BASH_UBUNTU16}_exec.sh ${COMMAND}"
}
