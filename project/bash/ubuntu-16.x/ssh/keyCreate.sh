#!/usr/bin/env bash

sshKeyCreateArgs() {
  _ARGUMENTS=(
    [0]='file f "File to store public key ex : /root/.ssh/example.key" true'
  )
}

sshKeyCreate() {
  ssh-keygen -t rsa -N "" -f ${FILE} -q
}
