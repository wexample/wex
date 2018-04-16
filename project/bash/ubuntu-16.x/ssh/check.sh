#!/usr/bin/env bash

sshCheckArgs() {
  _ARGUMENTS=(
    [0]='user u "User" true'
    [1]='host host "Host" true'
    [2]='key k "SSH Key to use" false'
  )
}

sshCheck() {
  local OPTIONS=''
  if [ "${KEY}" != "" ];then
    OPTIONS=" -i "${KEY}
  fi

  ssh ${OPTIONS} -q ${USER}@${HOST} exit
  local STATUS=$(echo $?)
  # Connection is up.
  if [ ${STATUS} == 0 ];then
    echo true
  else
    echo false
  fi
}
