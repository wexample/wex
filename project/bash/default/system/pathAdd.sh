#!/usr/bin/env bash

systemPathAddArgs() {
 _ARGUMENTS=(
   'new_path p "New path" true'
   'bashrc_path b "Bashrc path" false'
   'global_path_content g "Replace usage of global PATH variable" false'
 )
}

systemPathAdd() {
  # Convert slashes
  NEW_PATH=$(echo "${NEW_PATH}" | sed 's/\//\\\//g')

  if [[ $(wex var/filled -v=${GLOBAL_PATH_CONTENT}) ]];then
    PATH_CONTENT=${GLOBAL_PATH_CONTENT}
  else
    PATH_CONTENT=${PATH}
  fi

  # Search occurrence of new path.
  foundInBody=$(sed -n "s/\(.\{0,\}\):\(${NEW_PATH}\):\(.\{0,\}\)/\2/p" <<< ${PATH_CONTENT})
  foundAtEnd=$(sed -n "s/\(.\{0,\}\):\(${NEW_PATH}\)$/\2/p" <<< ${PATH_CONTENT})

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
  command=$(sed -e 's/[]\/$\{0,\}.^|[]/\\&/g' <<< "${command}")${NEW_PATH}

  # Add to bashrc.
  wex file/textAppendOnce -f="${BASHRC_PATH}" -l="${command}"
}
