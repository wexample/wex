#!/usr/bin/env bash

sshValidateArgs() {
  _DESCRIPTION='Connect to an SSH remote server. Useful to first connect and check arguments.'
  _ARGUMENTS=(
    'host h "Host" true'
    'port p "Port" true'
  )
}

sshValidate() {
  # Create a temporary inventory.
  wex server::inventory/write -n wex_command_host -h ${HOST} -p ${PORT}
  # Execute response.
  local RESPONSE=$(ansible all -m ping -k -i ${WEX_DIR_TMP}inventory)

  # Ansible ping succeed.
  if [ "$(echo ${RESPONSE} | grep "SUCCESS")" != "" ];then
    echo true
  else
    echo false
  fi
}
