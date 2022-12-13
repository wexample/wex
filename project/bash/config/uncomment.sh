#!/usr/bin/env bash

configUncommentArgs() {
 _ARGUMENTS=(
   'target_key k "Target key to uncomment" true'
   'separator s "Separator like space or equal sign, default space" false'
   'file f "File" true'
   'char c "Comment character" false'
 )
}

configUncomment() {
  SEPARATOR="$(wex config/processSeparator -s="${SEPARATOR}")"

  if [ -z "${CHAR+x}" ];then
    # Default space separator
    CHAR="#"
  fi;

  # Replace key with any # or space before it
  # with the same (captured value) without these chars.
  wex file/textReplace -r="s/^\([ ]\{0,\}\)[${CHAR}]\{1,\}\([ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)/\1\2/" -f=${FILE}
}
