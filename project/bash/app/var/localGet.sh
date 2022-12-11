#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    'name n "Variable name" true'
    'default d "Default value" false'
    'ask a "Message to ask user to, enable prompt if provided" false'
    'password p "Hide typed response when asking user" false'
    'required r "Ask again if empty" false'
    'save_default s "Save last value as default" false'
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

  local OUTPUT=$(wex var/get \
    -n="${NAME}" \
    -d="${DEFAULT}" \
    -a="${ASK}" \
    -p="${PASSWORD}" \
    -r="${REQUIRED}" \
    -f="${WEXAMPLE_SITE_LOCAL_VAR_STORAGE}")

  # Memorize last choice.
  if [ "${SAVE_DEFAULT}" == true ];then
    wex var/set -n="LAST_${NAME}" -v="${OUTPUT}"
  fi

  echo "${OUTPUT}"
}
