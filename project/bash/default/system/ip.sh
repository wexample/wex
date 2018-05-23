#!/usr/bin/env bash

systemIp() {
  if [ $(wex docker/isToolBox) ];then
    wex docker/ip
    return
  fi
  # May have several IP's
  IPS=($(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'))
  # Take the last one
  echo ${IPS[-1]}
}
