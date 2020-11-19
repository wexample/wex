#!/usr/bin/env bash

# Find first db service found.
dbDetect() {
  local ALLOWED=(mysql mysql8 postgres mariadb redis)
  local SERVICES=($(wex service/list))

  for SERVICE in ${SERVICES[@]}
  do
    for ALLOW in ${ALLOWED[@]}
    do
      if [ ${SERVICE} == ${ALLOW} ];then
        echo ${SERVICE}
        return
      fi
    done
  done
}