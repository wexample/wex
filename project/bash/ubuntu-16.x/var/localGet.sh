#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
  )
}

varLocalGet() {
  local LOCAL_STORAGE_FILE=${WEX_DIR_TMP}variablesLocalStorage

  if [ -f ${LOCAL_STORAGE_FILE} ];then
    # Eval whole file.
    eval $(cat ${LOCAL_STORAGE_FILE})
    # Get value
    local VALUE=$(eval 'echo ${'${NAME}'}')

    # Value not found.
    if [ "${VALUE}" == "" ]; then
      # Asking user enabled.
      if [ ! -z "${ASK+x}" ]; then
        local OPTIONS=''
        if [ ! -z "${PASSWORD+x}" ]; then
          OPTIONS='-s'
        fi

        read ${OPTIONS} -p "${ASK} : " VALUE
      else
        VALUE=DEFAULT
      fi
      # Store value.
      wex var/localSet -n=${NAME} -v=${VALUE}
    fi;

    echo ${VALUE}
  fi
}
