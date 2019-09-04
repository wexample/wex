#!/usr/bin/env bash

dockerIp() {
  # Docker IP is only localhost
  if [[ $(wex system/osName) == 'mac' ]];then
    echo "127.0.0.1"
    return
  fi

  if [[ $(command -v docker-machine) ]];then
    echo $(docker-machine ip)
  else
    echo $(wex system/ip)
  fi
}
