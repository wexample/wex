#!/usr/bin/env bash

configKeyExistsArgs() {
 _ARGUMENTS=(
   'target_key k "Target key to get" true'
   'separator s "Separator like space or equal sign, default space" false'
   'file f "File" true'
   'comments c "Search also into commented lines" false'
   'comments_only co "Search into commented lines only" false'
 )
}

configKeyExists() {
  local COMMENT_REGEX=""

  if [ "${COMMENTS}" = true ]; then
    # Zero or more
    COMMENT_REGEX='[#]\{0,\}'
  elif [ "${COMMENTS_ONLY}" = true ]; then
    COMMENT_REGEX='[#]\{1,\}'
  fi;

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  local RESULTS
  RESULTS=$(sed -n "s/^\([ ]\{0,\}${COMMENT_REGEX}[ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)/\1/p" ${FILE})

  if [ ${#RESULTS} -gt 0 ]; then
    echo true
    return
  fi;

  echo false
}
