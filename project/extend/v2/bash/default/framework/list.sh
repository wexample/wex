#!/usr/bin/env bash

frameworkListArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of framework" false'
  )
}

# dependency : php, composer
frameworkList() {

  if [[ -z "${DIR+x}" ]]; then
    # Get current dir.
    DIR=./
  fi;

  DIRS=($(ls -d ${WEX_DIR_BASH_DEFAULT}framework*))
  local FRAMEWORK_FOUND=()
  for FRAMEWORK_DIR in ${DIRS[@]}
  do
    FRAMEWORK_DIR_NAME=$(basename ${FRAMEWORK_DIR})
    if [ ${FRAMEWORK_DIR_NAME} != framework ];then
      # Get name.
      FRAMEWORK_NAME=${FRAMEWORK_DIR_NAME#framework}
      # Lower case first letter.
      FRAMEWORK_NAME=$(tr '[:upper:]' '[:lower:]' <<< ${FRAMEWORK_NAME:0:1})${FRAMEWORK_NAME:1}

      # There is a detection script
      # And it returns true
      if [ -f ${FRAMEWORK_DIR}"/"used.sh ] && [ $(wex ${FRAMEWORK_DIR_NAME}/used -d=${DIR}) == true ];then
        FRAMEWORK_FOUND+=(${FRAMEWORK_NAME})
      fi
    fi
  done

  echo ${FRAMEWORK_FOUND[@]}

}
