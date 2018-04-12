#!/usr/bin/env bash

userAdd() {
  user=${1}
  password=${2}
  group=${3}
  # Create a new super user.
  useradd -g ${group} -ms /bin/bash -p $(echo ${password} | openssl passwd -1 -stdin) ${user}
}
