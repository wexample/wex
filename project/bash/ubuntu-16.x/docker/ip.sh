#!/usr/bin/env bash

dockerIp() {
  if [[ $(command -v docker-machine) ]];then
    echo $(docker-machine ip)
  else
    echo $(wex system/ip)
  fi
}
