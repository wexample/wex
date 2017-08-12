#!/usr/bin/env bash

configKeyExists() {
  arguments=("$@")
  argumentsFiltered=()
  commentRegex=''

  # Function use mixed options types.
  # We first filter dashed option
  # and remove them from arguments.
  # Manage arguments
  for ((i=0;i<=${#@};i++));
  do
    case ${arguments[$i]} in
      -c|--commented)
        # Zero or more
        commentRegex='[#]*'
        ;;
      -co|--commented-only)
        # At least one
        commentRegex='[#]\+'
        ;;
      *)
      argumentsFiltered+=(${arguments[$i]})
    esac
  done

  TARGET_KEY=${argumentsFiltered[1]}
  SEPARATOR=${argumentsFiltered[2]}
  FILE=${argumentsFiltered[0]}

  # Prevent empty string
  if [ ${#TARGET_KEY} == 0 ]; then
    return
  fi;

  if [ -z ${SEPARATOR} ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  results=$(sed -n "s/^\([ ]*${commentRegex}[ ]*${TARGET_KEY}[ ]*${SEPARATOR}\+[ ]*\)/\1/p" ${FILE})

  if [[ ${#results} > 0 ]]; then
    echo true
    return
  fi;

  echo false
}
