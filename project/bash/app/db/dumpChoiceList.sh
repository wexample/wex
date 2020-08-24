#!/usr/bin/env bash

dbDumpChoiceList() {
  local FILES
  local CHOICES
  FILES=($(ls mysql/dumps))

  if [[ ${#FILES[@]} == 0 ]];then
    echo "No dump found."
    return
  fi;

  # iterate through array using a counter
  for ((i=0; i<${#FILES[@]}; i++)); do
    DISPLAY=$((i+1))

    if [ "${CHOICES}" != "" ];then
      CHOICES+=","
    fi

    CHOICES+="${FILES[$i]}"
  done

  wex prompt/choice -c="${CHOICES}"

}
