#!/usr/bin/env bash

textCamelCaseArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to work on" true'
    [1]='uppercase u "Uppercase the first letter" false'
  )
}

textCamelCase() {
  if [[ ${UPPERCASE} == true ]];then
    echo -e "${TEXT}" | sed -E 's/(^|_)([a-z])/\U\2/g'
  else
    echo -e "${TEXT}" | sed -E 's/_([a-z])/\U\1/g' | sed -E 's/^([A-Z])/\l\1/'
  fi;
}