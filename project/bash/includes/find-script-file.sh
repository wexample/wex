#!/usr/bin/env bash

. "${WEX_DIR_BASH}globals.sh"

WEX_SCRIPT_CALL_NAME="${1}"

# Allow specified context.
if [[ ${1} == *"::"* ]]; then
  SPLIT=($(echo "${1}"| tr ":" "\n"))

  WEX_NAMESPACE_TEST=${SPLIT[0]}
  WEX_SCRIPT_CALL_NAME=${SPLIT[1]}
# Check if we are on an "app" context (.wex dir in calling folder).
elif [ -f "${PWD}/.wex" ]; then
  WEX_NAMESPACE_TEST=${WEX_NAMESPACE_APP}
fi;

WEX_SCRIPT_DIR=${WEX_DIR_BASH}${WEX_NAMESPACE_TEST}/${WEX_SCRIPT_CALL_NAME}
WEX_SCRIPT_FILE=${WEX_SCRIPT_DIR}.sh
WEX_SCRIPT_METHOD_NAME=$(_wexMethodName "${WEX_SCRIPT_CALL_NAME}")
WEX_SCRIPT_METHOD_ARGS_NAME=${WEX_SCRIPT_METHOD_NAME}"Args";

# Use main script if still not exists.
if [ -f "${WEX_SCRIPT_FILE}" ] || [ -d "${WEX_SCRIPT_DIR}" ]; then
  WEX_NAMESPACE=${WEX_NAMESPACE_TEST}
else
  WEX_NAMESPACE=${WEX_NAMESPACE_DEFAULT}
  # Search into wex local folder.
  WEX_SCRIPT_FILE=${WEX_DIR_BASH}${WEX_NAMESPACE_DEFAULT}/${WEX_SCRIPT_CALL_NAME}.sh
fi;

# Load namespace init file.
. "${WEX_DIR_BASH}${WEX_NAMESPACE}/init.sh"

export WEX_NAMESPACE_TEST
export WEX_SCRIPT_DIR
export WEX_SCRIPT_FILE
export WEX_SCRIPT_METHOD_NAME
export WEX_SCRIPT_METHOD_ARGS_NAME