#!/usr/bin/env bash

remoteExecArgs() {
  _ARGUMENTS=(
    [0]='ssh_user_custom u "SSH User" false'
    [1]='ssh_private_key_custom k "SSH Private key" false'
    [2]='ssh_host_custom host "Host to connect to" false'
    [3]='ssh_port_custom p "SSH Port" false'
    [4]='environment e "Environment to connect to" true'
    [5]='shell_script s "Command to execute from shell, relative to site directory" true'
    [6]='dir d "Remote directory (site directory by default)" false'
  )
}

remoteExec() {
  echo wex remote/connexion -e=${ENVIRONMENT} ${WEX_ARGUMENTS}
  # Prevent to set credentials globally
  local SSH_CONNEXION=$(wex remote/connexion -e=${ENVIRONMENT} ${WEX_ARGUMENTS})

  # Load credentials stored into config
  # TODO used ?wex config/load

  if [ "${DIR}" != "" ];then
    local SITE_PATH_ROOT=${DIR}
  else
    local SITE_PATH_ROOT=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${SITE_NAME}/
  fi

  ssh -oLogLevel=QUIET ${SSH_CONNEXION} "cd ${SITE_PATH_ROOT} && ${SHELL_SCRIPT}"
}
