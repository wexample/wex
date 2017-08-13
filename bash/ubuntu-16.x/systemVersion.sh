#!/usr/bin/env bash

systemVersion() {
  if [ $(wexample fileExists /etc/*-release) ]; then
    . /etc/*-release
    echo ${PRETTY_NAME}
    return
  fi;
  uname -mrs
}
