#!/usr/bin/env bash

export WEX_CORE_VERSION=3
export WEX_DIR_BASH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/
export WEX_DIR_ROOT=$(realpath ${WEX_DIR_BASH}"../")"/"
export WEX_DIR_INSTALL=$(realpath ${WEX_DIR_ROOT}"../")"/"
export WEX_DIR_EXTEND=${WEX_DIR_ROOT}extend/
export WEX_NAMESPACE_DEFAULT="default"
export WEX_NAMESPACE_APP="app"
export BASHRC_PATH=~/.bashrc

# Used both in core and autocomplete
_wex_find_namespace() {
  export WEX_NAMESPACE_TEST=
  # Allow specified context.
  if [[ ${1} == *"::"* ]]; then
    SPLIT=($(echo ${1}| tr ":" "\n"))
    export WEX_NAMESPACE_TEST=${SPLIT[0]}
    export WEX_SCRIPT_CALL_NAME=${SPLIT[1]}
  # Check if we are on a "wexample" context (.wex file in calling folder).
  elif [ -f ${PWD}"/.wex" ]; then
    export WEX_NAMESPACE_TEST=${WEX_NAMESPACE_APP}
  fi;
}