#!/usr/bin/env bash

sshValidateArgs() {
  _DESCRIPTION='Connect to an SSH remote server. Useful to first connect and check arguments.'
  _ARGUMENTS=(
    [0]='host h "Host" true'
    [1]='port p "Port" true'
  )
}

sshValidate() {
  # Create a temporary inventory.
  echo ${HOST} ansible_port=${PORT} ansible_python_interpreter=/usr/bin/python3 > ${WEX_DIR_TMP}inventory
  # Execute response.
  local RESPONSE=$(ansible all -m ping -k -i ${WEX_DIR_TMP}inventory)

  # Ansible ping succeed.
  if [ "$(echo ${RESPONSE} | grep "SUCCESS")" != "" ];then
    echo true
  else
    echo false
  fi
}
