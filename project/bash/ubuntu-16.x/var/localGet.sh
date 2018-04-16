#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
    [4]='required r "Ask again if empty" false'
    [5]='file f "Storage file path" false'
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
  wexLoadVariables
  # Is defined or not, even empty value.
  local EXISTS=$(eval '[[ ! -z "${'${NAME}'+x}" ]] && echo true || echo false')
  # Get value
  local VALUE=$(eval 'echo ${'${NAME}'}')
  local OUTPUT=${VALUE}

  # Value is empty, use default.
  if [ "${VALUE}" == "" ] && [ "${EXISTS}" == false ];then
    OUTPUT="${DEFAULT}"
  fi

  # Value is still empty and not defined or required.
  if [ "${VALUE}" == "" ] && ([ "${EXISTS}" == false ] || [ "${REQUIRED}" == true ]) && [ ! -z "${ASK+x}" ];then
    while true;do
      local OPTIONS=''
      local MESSAGE="${ASK}"

      if [ "${PASSWORD}" == true ]; then
        OPTIONS='-s'
      fi

      if [ "${DEFAULT}" != "" ]; then
        MESSAGE=${MESSAGE}" ("${DEFAULT}")"
      fi

      read ${OPTIONS} -p "${MESSAGE} : " OUTPUT

      # Value is empty, use default.
      if [ "${OUTPUT}" == "" ];then
        OUTPUT="${DEFAULT}"
      fi

      # Stop if value is filled or allowed as empty.
      if [ "${OUTPUT}" != "" ] || [ "${REQUIRED}" != true ];then
        break
      fi
    done
  fi

  # Value has changed or is not saved.
  if [ "${OUTPUT}" != "${VALUE}" ] || [ ${EXISTS} == false ];then
    # Store value.
    wex var/localSet -n="${NAME}" -v="$(printf "%q" "${OUTPUT}")" -f=${FILE}
  fi

  echo "${OUTPUT}"
}
