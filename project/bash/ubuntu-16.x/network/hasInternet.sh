#!/usr/bin/env bash

networkHasInternet() {
  local IP=$(ip r | grep default | cut -d ' ' -f 3)

  if [ "${IP}" != "" ];then
    ping -q -w 1 -c 1 ${IP} > /dev/null && echo true || echo false
    return
  fi

  echo false
}