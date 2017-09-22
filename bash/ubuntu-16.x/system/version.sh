#!/usr/bin/env bash

systemVersion() {
  if [ $(wexample fileExists /etc/*-release) ]; then
    . /etc/*-release
    echo ${PRETTY_NAME}
    return
  elif [ $(wexample fileExists /proc/version) ]; then
    cat /proc/version
  else
    uname -mrs
  fi;
}
