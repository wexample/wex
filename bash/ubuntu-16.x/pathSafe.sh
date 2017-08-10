#!/usr/bin/env bash

pathSafe() {
  osName=$(wexample bashOsName)

  # Os is windows
  if [ ${osName} == "windows" ];then
    firstLetter="$(echo ${1} | head -c 1)"
    # Path is not already converted.
    if [ ${firstLetter} == "/" ];then
      echo $(wexample pathPosixToWindows ${1});
      return
    fi;
  fi;

  echo ${1};
}
