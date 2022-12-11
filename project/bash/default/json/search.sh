#!/usr/bin/env bash

jsonSearchArgs() {
 _ARGUMENTS=(
   [0]='json j "Content to search into" true'
   [1]='search s "Search key" true'
   [2]='value v "Search value" true'
   [3]='key k "Key value to return" true'
 )
}

# Ex : return the "id" (key) of a json item containing
# another key (search) which have a certain value.
jsonSearch() {
  # Get lis of enabled keys
  local RESULTS=($(wex json/find -k=${KEY} -j="${JSON}"))
  local VALUES=$(wex json/find -k=${SEARCH} -j="${JSON}")
  local VALUE_LENGTH=${#VALUE}
  local COUNT=0

  while read -r LINE; do
    local CUT=$(echo ${LINE} | head -c${VALUE_LENGTH})
    # Key found.
    if [ "${CUT}" == "${VALUE}" ];then
      # Print expected value.
      echo ${RESULTS[${COUNT}]}
      return
    fi

    ((COUNT++))
  done <<< "${VALUES}"
}