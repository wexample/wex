#!/usr/bin/env bash

userSetSudoArgs() {
  _ARGUMENTS=(
    [0]='username u "User" true'
  )
}

userSetSudo() {
  usermod -aG sudo ${USERNAME}
}
