#!/usr/bin/env bash

configCommentArgs() {
  # shellcheck disable=SC2034
  _ARGUMENTS=(
   'target_key k "Target key to comment" true'
   'separator s "Separator like space or equal sign, default space" false'
   'file f "File" true'
   'char c "Comment character" false'
 )
}

configComment() {
  SEPARATOR="$(wex-exec default::config/processSeparator -s="${SEPARATOR}")"

  if [ -z "${CHAR+x}" ];then
    # Default space separator
    CHAR="#"
  fi;

  # Replace key beginning the line or having space(s) before it
  # by the same with a # before it
  wex-exec file/textReplace -r="s/^\([ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)/${CHAR}\1/" -f=${FILE}
}
