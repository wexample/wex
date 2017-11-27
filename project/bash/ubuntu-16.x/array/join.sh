#!/usr/bin/env bash

arrayJoinArgs() {
  _ARGUMENTS=(
    [0]='array a "Array content" true'
    [1]='separator s "Separator" false'
  )
}

arrayJoin() {
  ARRAY=(${ARRAY})
  OUTPUT=""

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=""
  fi;

  FIRST=true

  for ITEM in ${ARRAY[@]}
  do
    if [[ ${FIRST} == true ]];then
      FIRST=false
    else
      OUTPUT+=${SEPARATOR}
    fi

    OUTPUT+=${ITEM}
  done;

  echo ${OUTPUT}
}
