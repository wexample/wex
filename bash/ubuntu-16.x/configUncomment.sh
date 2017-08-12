#!/usr/bin/env bash

configUncomment() {
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

  # Replace key with any # or space before it
  # with the same (captured value) without these chars.
  wexample fileTextReplace "s/^[ #]*\(${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\)/\1/" ${FILE}
}
