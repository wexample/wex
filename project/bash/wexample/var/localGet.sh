#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
    [4]='required r "Ask again if empty" false'
    [5]='save_default s "Save last value as default" false'
  )
}

varLocalGet() {
  wexampleSiteInitLocalVariables
  . ${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}

  # Default is not defined.
  if [ "${SAVE_DEFAULT}" == true ] && [ "${DEFAULT}" == "" ];then
    wexLoadVariables
    # Get last saved value.
    DEFAULT=$(eval 'echo ${LAST_'${NAME}'}')
  fi

  local OUTPUT=$(wex default::var/localGet -d="${DEFAULT}" ${WEX_ARGUMENTS} -f=./tmp/variablesLocalStorage)

  # Memorize last choice.
  if [ "${SAVE_DEFAULT}" == true ];then
    wex default::var/localSet -n="LAST_${NAME}" -v="${OUTPUT}"
  fi

  echo ${OUTPUT}
}
