#!/usr/bin/env bash

configCommentArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to comment" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
 )
}

configComment() {

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  # Replace key beginning the line or having space(s) before it
  # by the same with a # before it
  wex file/textReplace "s/^\([ ]*${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\)/#\1/" ${FILE}
}
