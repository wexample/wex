#!/usr/bin/env bash

systemPathAdd() {
  NEW_PATH=${1}
  # Convert slashes
  NEW_PATH=$(echo "${NEW_PATH}" | sed 's/\//\\\//g')
  BASHRC_PATH=${2}

  # Search occurrence of new path.
  foundInBody=$(sed -n "s/\(.*\):\(${NEW_PATH}\):\(.*\)/\2/p" <<< ${PATH})
  foundAtEnd=$(sed -n "s/\(.*\):\(${NEW_PATH}\)$/\2/p" <<< ${PATH})

  # Return command to execute globally
  if [ "${foundInBody}" == "" ] && [ "${foundAtEnd}" == "" ]; then
    # Print command to add, need to execute it into global context.
    echo 'export PATH=$PATH:'${1}
  fi

  # Default pathg
  if [ ${BASHRC_PATH} == '' ]; then
    BASHRC_PATH=~/.bashrc
  fi;

  command='export PATH=\$PATH:'
  # Protect arguments by escaping special chars.
  command=$(sed -e 's/[]\/$*.^|[]/\\&/g' <<< "${command}")${1}

  # Add to bashrc.
  wexample fileTextAppendOnce "${BASHRC_PATH}" "${command}"

}
