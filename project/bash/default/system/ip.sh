#!/usr/bin/env bash

systemIp() {
  if [ "$(wex docker/isToolBox)" = true ];then
    wex docker/ip
    return
  fi
  # Enforce language for parsing.
  export LC_ALL=C
  # May have several IP's
  IPS=($(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'))
  # Revert to default language.
  unset LC_ALL
  # Take the last one
  echo "${IPS[-1]}"
}
