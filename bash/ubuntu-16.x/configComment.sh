#!/usr/bin/env bash

configComment() {
  TARGET_KEY=${2}
  SEPARATOR=${3}
  FILE=${1}

  # Prevent empty string
  if [ ${#TARGET_KEY} == 0 ]; then
    return
  fi;

  if [ -z "${3+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Replace key beginning the line or having space(s) before it
  # by the same with a # before it
  wexample fileTextReplace "s/^\([ ]*${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\)/#\1/" ${FILE}
}
