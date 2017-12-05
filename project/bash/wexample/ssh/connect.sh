#!/usr/bin/env bash

sshConnectArgs() {
 _ARGUMENTS=(
   [0]='dir_site d "Local root site directory" false'
 )
}

sshConnect() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # For now, the username is gitlab,
  # but we should use allowed account for current environment.
  wex wexample::site/deployCredentials -d=${DIR_SITE}

  ssh-keygen -R ${DEPLOY_IPV4}

  # Go do site path
  # Then execute script from _exec.sh tool of wexample.
  ssh -p${DEPLOY_PORT} ${DEPLOY_USER}@${DEPLOY_IPV4}
}

