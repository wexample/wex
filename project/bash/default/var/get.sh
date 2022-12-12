#!/usr/bin/env bash

varGetArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'default d "Default value" false'
    'ask a "Message to ask user to, enable prompt if provided" false'
    'password p "Hide typed response when asking user" false'
    'required r "Ask again if empty" false'
    'file f "Storage file path" false'
  )
}

varGet() {
  # If no file specified
  if [ "${FILE}" = "" ];then
    # Use wex tmp folder
    FILE=${WEX_TMP_GLOBAL_VAR}
  fi

  touch ${FILE}

  # Remove variable
  local EXISTS=$(eval '[[ ! -z "${'${NAME}'+x}" ]] && echo true || echo false')
  if [ "${EXISTS}" == false ];then
    eval 'unset ${'${NAME}'}'
  fi

  # Eval whole file.
  _wexLoadVariables
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
  if [ "${VALUE}" == "" ] && ([ "${EXISTS}" == false ] || [ "${REQUIRED}" == true ]) && [ "${ASK}" != "" ];then
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
    wex var/set -n="${NAME}" -v="$(printf "%q" "${OUTPUT}")" -f=${FILE}
  fi

  echo "${OUTPUT}"
}
