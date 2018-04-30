#!/usr/bin/env bash

varFilledArgs() {
  _ARGUMENTS=(
    [0]='value v "Variable content to test if empty or not" true'
    [1]='show_false s "Prints false if empty, if not, it allows to use this method into condition without testing returned value" false'
  )
}

varFilled() {
  if [ ! -z "${VALUE:+x}" ];then
    echo true
  # Print false only if expected
  elif [[ ${SHOW_FALSE} == true ]];then
    echo false
  fi;
}
