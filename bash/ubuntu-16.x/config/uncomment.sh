#!/usr/bin/env bash

configUncommentArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to uncomment" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
 )
}

configUncomment() {

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Replace key with any # or space before it
  # with the same (captured value) without these chars.
  wex file/textReplace -r="s/^[ #]*\(${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\)/\1/" -f=${FILE}
}
