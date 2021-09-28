#!/usr/bin/env bash

remoteGetSshUsername() {
  . .wex
  . .env

  if [ "${SSH_USERNAME}" = "" ];then
    SSH_USERNAME=$(whoami)
  fi

  echo "${SSH_USERNAME}"
}