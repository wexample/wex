#!/usr/bin/env bash

playbookExecArgs() {
  _DESCRIPTION='Execute a given wex playbook for the host'
  _ARGUMENTS=(
    [0]='host h "Host" true'
    [1]='port p "Port" true'
    [2]='name n "Playbook name" true'
  )
}

playbookExec() {
  local PLAYBOOK_DIR=${WEX_DIR_SAMPLES}ansible/playbooks/${NAME}/provision.yml

  if [ ! -f ${PLAYBOOK_DIR} ];then
    _wexError "Playbook not found " "Missing folder ${PLAYBOOK_DIR}"
    exit
  fi

  # Create a temporary inventory.
  wex server::inventory/write -n wex_command_host -h ${HOST} -p ${PORT}
  # Execute playbook
  ansible-playbook -k ${PLAYBOOK_DIR} -i ${WEX_DIR_TMP}inventory
}
