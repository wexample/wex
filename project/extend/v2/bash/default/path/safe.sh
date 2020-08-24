#!/usr/bin/env bash

pathSafeArgs() {
  _ARGUMENTS=(
    [0]='path_name p "Path" true'
  )
}

pathSafe() {
  osName=$(wex system/os)

  # Os is windows
  if [[ ${osName} == "windows" ]];then
    firstLetter="$(echo ${PATH_NAME} | head -c 1)"
    # Path is not already converted.
    if [ ${firstLetter} == "/" ];then
      echo $(wex path/posixToWindows -p=${PATH_NAME});
      return
    fi;
  fi;

  echo ${PATH_NAME};
}
