#!/usr/bin/env bash

networkHasInternet() {
  local IP=$(ip r | grep default | cut -d ' ' -f 3)
  local RETURN='false'
  if [ "${IP}" != "" ];then
    local RETURN=$(ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo true || echo error)

    if [ ${RETURN} == 'error' ];then
      if ping -c 1 wexample.com >> /dev/null 2>&1; then
        RETURN=true
      # Okay, try with a serious website
      elif ping -c 1 google.com >> /dev/null 2>&1; then
        RETURN=true
      fi
    fi
  fi

  echo ${RETURN}
}