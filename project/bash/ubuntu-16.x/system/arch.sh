#!/usr/bin/env bash

systemArch() {
  MACHINE_TYPE=`uname -m`
  if [ ${MACHINE_TYPE} == 'x86_64' ]; then
    echo 64
  else
    echo 32
  fi
}
