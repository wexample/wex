#!/usr/bin/env bash

arrayJoinArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION="Join array values (space separated) with given separator"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'array a "Array content" true'
    'separator s "Separator" false'
  )
}

arrayJoin() {
  local ARRAY=(${ARRAY})

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=""
  fi;

  local FIRST=true
  local OUTPUT=""

  for ITEM in "${ARRAY[@]}"
  do
    if [ "${FIRST}" = true ];then
      FIRST=false
    else
      OUTPUT+=${SEPARATOR}
    fi

    OUTPUT+=${ITEM}
  done;

  echo "${OUTPUT}"
}
