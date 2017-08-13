#!/usr/bin/env bash

bashAddToPath() {
  NEW_PATH=${1}
  # Convert slashes
  NEW_PATH=$(echo "${NEW_PATH}" | sed 's/\//\\\//g')

  # Search occurrence of new path.
  foundInBody=$(sed -n "s/\(.*\):\(${NEW_PATH}\):\(.*\)/\2/p" <<< ${PATH})
  foundAtEnd=$(sed -n "s/\(.*\):\(${NEW_PATH}\)$/\2/p" <<< ${PATH})

  command="export PATH=\044PATH":${1}

  # Return command to execute globally
  if [ "${foundInBody}" == "" ] && [ "${foundAtEnd}" == "" ]; then
    # Print command to add, need to execute it into global context.
    echo ${command}
  fi

  # Add to bashrc.
  wexample fileTextAppendOnce ~/.bashrc "${command}\n"

  cat ~/.bashrc
}
