#!/usr/bin/env bash

configKeyExistsArgs() {
 _ARGUMENTS=(
   [0]='target_key k "Target key to get" true'
   [1]='separator s "Separator like space or equal sign, default space" false'
   [2]='file f "File" true'
   [3]='comments c "Search also into commented lines" false'
   [4]='comments_only co "Search into commented lines only" false'
 )
}

configKeyExists() {
  COMMENT_REGEX=''

  if [[ ${COMMENTS} == true ]]; then
    # Zero or more
    COMMENT_REGEX='[#]\{0,\}'
  elif [[ ${COMMENTS_ONLY} == true ]]; then
    COMMENT_REGEX='[#]\{1,\}'
  fi;

  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  results=$(sed -n "s/^\([ ]\{0,\}${COMMENT_REGEX}[ ]\{0,\}${TARGET_KEY}[ ]\{0,\}${SEPARATOR}[ ]\{0,\}\)/\1/p" ${FILE})

  if [[ ${#results} > 0 ]]; then
    echo true
    return
  fi;

  echo false
}
