#!/usr/bin/env bash

# Find first db service found.
dbDetect() {
  local ALLOWED=(mysql mysql8 postgres mariadb redis)
  local SERVICES=($(wex service/list))

  for SERVICE in ${SERVICES[*]}
  do
    for ALLOW in ${ALLOWED[*]}
    do
      if [ "${SERVICE}" = "${ALLOW}" ];then
        # TODO Temporary fix to support mysql8 calling mysql methods
        #      We need to find a better way to find contextual methods according db type
        if [ "${SERVICE}" = "mysql8" ];then
          echo "mysql"
          return
        fi

        echo "${SERVICE}"
        return
      fi
    done
  done
}