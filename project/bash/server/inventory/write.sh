#!/usr/bin/env bash

inventoryWriteArgs() {
  _DESCRIPTION='Write an inventory file with given host informations.'
  _ARGUMENTS=(
    'name n "The host name in format (a-zA-Z_)" true'
    'host h "Host" true'
    'port p "Port" true'
  )
}

inventoryWrite() {
  # Host name
  echo "[${NAME}]" > ${WEX_DIR_TMP}inventory
  # Entry
  echo ${HOST} ansible_port=${PORT} ansible_python_interpreter=/usr/bin/python3 >> ${WEX_DIR_TMP}inventory
}
