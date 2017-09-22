#!/usr/bin/env bash

systemPathAddArgs() {
 _ARGUMENTS=(
   [0]='new_path p "New path" true'
   [1]='bashrc_path b "Bashrc path" false'
 )
}

systemPathAdd() {
  # Convert slashes
  NEW_PATH=$(echo "${NEW_PATH}" | sed 's/\//\\\//g')

  # Search occurrence of new path.
  foundInBody=$(sed -n "s/\(.*\):\(${NEW_PATH}\):\(.*\)/\2/p" <<< ${PATH})
  foundAtEnd=$(sed -n "s/\(.*\):\(${NEW_PATH}\)$/\2/p" <<< ${PATH})

  # Return command to execute globally
  if [ "${foundInBody}" == "" ] && [ "${foundAtEnd}" == "" ]; then
    # Print command to add, need to execute it into global context.
    echo 'export PATH=$PATH:'${NEW_PATH}
  fi

  # Default pathg
  if [ "${BASHRC_PATH}" == '' ]; then
    BASHRC_PATH=~/.bashrc
  fi;

  command='export PATH=\$PATH:'
  # Protect arguments by escaping special chars.
  command=$(sed -e 's/[]\/$*.^|[]/\\&/g' <<< "${command}")${NEW_PATH}

  # Add to bashrc.
  wex file/textAppendOnce -f="${BASHRC_PATH}" -l="${command}"

}
