#!/usr/bin/env bash

configCommentArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to comment" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
   [3]='char c "Comment character" false'
 )
}

configComment() {

  SEPARATOR="$(wex config/processSeparator -s="${SEPARATOR}")"

  if [ -z "${CHAR+x}" ];then
    # Default space separator
    CHAR="#"
  fi;

  # Replace key beginning the line or having space(s) before it
  # by the same with a # before it
  wex file/textReplace -r="s/^\([ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)/${CHAR}\1/" -f=${FILE}
}
