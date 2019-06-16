#!/usr/bin/env bash

dbDumpChooseList() {
  FILES=($(ls mysql/dumps))

  if [[ ${#FILES[@]} == 0 ]];then
    echo "No dump found."
    return
  fi;

  echo ""
  # iterate through array using a counter
  for ((i=0; i<${#FILES[@]}; i++)); do
    DISPLAY=$((i+1))
    echo -e "\t (${DISPLAY}) ${FILES[$i]}"
  done
  echo ""

}
