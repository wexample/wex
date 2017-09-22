#!/usr/bin/env bash

packageExistsArgs() {
 _ARGUMENTS=(
   [0]='name n "Package name to find" false'
 )
}

packageExists() {
  # Method works both on linux and windows.
  hash ${NAME} 2>/dev/null
  AVAILABLE=$?
  if [ ${AVAILABLE} -eq 0 ]; then
    echo true
   else
    echo false
  fi;
}
