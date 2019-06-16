#!/usr/bin/env bash

sshCheckArgs() {
  _ARGUMENTS=(
    [0]='user u "User" true'
    [1]='host h "Host" true'
    [2]='port p "Port" true'
    [3]='key k "SSH Key to use" false'
  )
}

sshCheck() {
  local OPTIONS=''
  if [ "${KEY}" != "" ];then
    OPTIONS=" -i "${KEY}
  fi

  if [ "${PORT}" == "" ];then
    PORT=22
  fi

  ssh ${OPTIONS} -q ${USER}@${HOST} -p ${PORT} exit

  local STATUS=$(echo $?)
  # Connection is up.
  if [ ${STATUS} == 0 ];then
    echo true
  else
    echo false
  fi
}
