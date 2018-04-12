#!/usr/bin/env bash

systemVersion() {
  if [ $(wex file/exists -f=/etc/*-release) == true ]; then
    . /etc/*-release
    echo ${PRETTY_NAME}
    return
  elif [ $(wex file/exists -f=/proc/version) == true ]; then
    cat /proc/version
  else
    uname -mrs
  fi;
}
