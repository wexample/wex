#!/usr/bin/env bash

userCreateArgs() {
  _ARGUMENTS=(
    [0]='user u "User" true'
    [1]='group g "Group" true'
    [2]='password p "Password" true'
  )
}

userCreate() {
  if [ "${GROUP}" == "" ];then
    local GROUP=${USER}
  fi

  # Create a new super user.
  useradd -g ${GROUP} -ms /bin/bash -p $(echo ${PASSWORD} | openssl passwd -1 -stdin) ${USER}
}
