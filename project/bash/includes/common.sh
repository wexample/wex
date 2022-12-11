#!/usr/bin/env bash

# Used both in core and autocomplete
_wexFindNamespace() {
  export WEX_NAMESPACE_TEST=
  # Allow specified context.
  if [[ ${1} == *"::"* ]]; then
    SPLIT=($(echo ${1}| tr ":" "\n"))

    export WEX_NAMESPACE_TEST=${SPLIT[0]}
    export WEX_SCRIPT_CALL_NAME=${SPLIT[1]}
  # Check if we are on a "wexample" context (.wex file in calling folder).
  elif [ -f "${PWD}/.wex" ]; then
    export WEX_NAMESPACE_TEST=${WEX_NAMESPACE_APP}
  fi;
}

_wexFindScriptFile() {
  export WEX_SCRIPT_DIR=${WEX_DIR_BASH}${WEX_NAMESPACE_TEST}/${WEX_SCRIPT_CALL_NAME}
  export WEX_SCRIPT_FILE=${WEX_SCRIPT_DIR}.sh
  export WEX_SCRIPT_METHOD_NAME=$(_wexMethodName "${WEX_SCRIPT_CALL_NAME}")
  export WEX_SCRIPT_METHOD_ARGS_NAME=${WEX_SCRIPT_METHOD_NAME}"Args";

  # Use main script if still not exists.
  if [ -f "${WEX_SCRIPT_FILE}" ] || [ -d "${WEX_SCRIPT_DIR}" ]; then
    export WEX_NAMESPACE=${WEX_NAMESPACE_TEST}
  else
    export WEX_NAMESPACE=${WEX_NAMESPACE_DEFAULT}
    # Search into wexample local folder.
    export WEX_SCRIPT_FILE=${WEX_DIR_BASH}${WEX_NAMESPACE_DEFAULT}/${WEX_SCRIPT_CALL_NAME}.sh
  fi;

  # Load namespace init file.
  . "${WEX_DIR_BASH}${WEX_NAMESPACE}/init.sh"
}

_wexMethodName() {
  local SPLIT=(${1//// })
  echo ${SPLIT[0]}$(_wexUpperCaseFirstLetter "${SPLIT[1]}")
}

_wexTruncate() {
  local MAX_MIDTH
  MAX_WIDTH=$(("${WEX_SCREEN_WIDTH}" - "${WEX_TRUCATE_SPACE}" - ${2}))

  if [ "${#1}" -gt "${MAX_WIDTH}" ];then
    echo "$(echo "${1}" | cut -c -"${MAX_WIDTH}")${WEX_COLOR_GRAY}...${WEX_COLOR_RESET} "
  else
    echo "${1}"
  fi
}

_wexUpperCaseFirstLetter() {
  echo $(tr '[:lower:]' '[:upper:]' <<< ${1:0:1})${1:1}
}