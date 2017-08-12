#!/usr/bin/env bash

packageIsInstalled() {
  if [ $(dpkg-query -W -f='${Status}' ${1} 2>/dev/null | grep -c "ok installed") == 1 ]; then
    echo true
    return
  fi;

  echo false
}
