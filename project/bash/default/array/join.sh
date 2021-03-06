#!/usr/bin/env bash

arrayJoinArgs() {
  _DESCRIPTION="Join array values (space separated) with given separator"
  _ARGUMENTS=(
    'array a "Array content" true'
    'separator s "Separator" false'
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
