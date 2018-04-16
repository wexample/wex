#!/usr/bin/env bash

sshConnectArgs() {
  _ARGUMENTS=(
    [0]='ssh_user_custom u "SSH User" false'
    [1]='ssh_private_key_custom k "SSH Private key" false'
    [2]='ssh_host_custom host "Host to connect to" false'
    [3]='ssh_port_custom p "SSH Port" false'
    [4]='environment e "Environment to connect to" true'
  )
}

sshConnect() {
  # Prevent to set credentials globally
  local SSH_CONNEXION=$(wex ssh/connexion -e=${ENVIRONMENT} ${WEX_ARGUMENTS})
  ssh -oStrictHostKeyChecking=no ${SSH_CONNEXION}
}
