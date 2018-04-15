#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
    [4]='file f "Storage file path" false'
  )
}

varLocalGet() {
  # If no file specified
  if [ -z "${FILE+x}" ]; then
    # Use wex tmp folder
    FILE=${WEX_DIR_TMP}variablesLocalStorage
  fi

  if [ ! -f ${FILE} ];then
    touch ${FILE}
  fi

  # Eval whole file.
  eval $(cat ${FILE})
  # Get value
  local VALUE=$(eval 'echo ${'${NAME}'}')

  # Value not found.
  if [ "${VALUE}" == "" ]; then
    # Asking user enabled.
    if [ ! -z "${ASK+x}" ]; then
      local OPTIONS=''
      if [ "${PASSWORD}" == true ]; then
        OPTIONS='-s'
      fi

      read ${OPTIONS} -p "${ASK} : " VALUE
    else
      VALUE=DEFAULT
    fi

    # Store value.
    wex var/localSet -n="${NAME}" -v="$(printf "%q" "${VALUE}")"

    echo ${VALUE}
  else
    echo "${VALUE}"
  fi;
}
