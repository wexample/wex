#!/usr/bin/env bash

playbookExecArgs() {
  _DESCRIPTION='Execute a given wex playbook for the host'
  _ARGUMENTS=(
    'host h "Host" true'
    'port p "Port" true 22'
    'name n "Playbook name" true'
    'user u "User" false root'
    'password pw "Password" false'
    'vars v "Extra variables" false'
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
