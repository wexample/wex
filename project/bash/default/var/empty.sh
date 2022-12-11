#!/usr/bin/env bash

varEmptyArgs() {
  _ARGUMENTS=(
    [0]='value v "Variable content to test if empty or not" true'
    [1]='show_false s "Prints false if empty, if not, it allows to use this method into condition without testing returned value" false'
  )
}

varEmpty() {
  if [[ $(wex var/filled -v="${VALUE}" -s) == false ]];then
    echo true
  # Print false only if expected
  elif [[ ${SHOW_FALSE} == true ]];then
    echo false
  fi;
}
