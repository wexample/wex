#!/usr/bin/env bash

# TODO If we want to allow switching user (non sudo to sudo) during scripts executions
#      we need to execute to write out this configuration variable in an external file
#      then reload only the built version of the variable.
#      For example, it will prevent to disable the "quiet mode"
#      when executing method as sudo user inside a non sudo script.

WEX_DIR_BASH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/
WEX_DIR_ROOT=$(dirname ${WEX_DIR_BASH})"/"
WEX_DIR_INSTALL=$(dirname ${WEX_DIR_ROOT})"/"
# /opt can't be mounted on macos, using Users instead.
WEX_WEXAMPLE_DIR_PROXY=$([[ "$(uname -s)" == Darwin ]] && echo /Users/.wex/server/ || echo /opt/wex_server/)

export BASHRC_PATH=~/.bashrc

export WEX_CORE_VERSION=3.3
export WEX_VERSION_FALLBACK=2.0.0
export WEX_DIR_BASH
export WEX_DIR_ROOT
export WEX_DIR_INSTALL
export WEX_DIR_EXTEND=${WEX_DIR_ROOT}extend/
export WEX_DIR_TMP=${WEX_DIR_ROOT}tmp/
export WEX_DIR_SAMPLES=${WEX_DIR_ROOT}samples/
export WEX_NAMESPACE_DEFAULT="default"
export WEX_NAMESPACE_APP="app"
export WEX_APP_DIR=""
export WEX_WEXAMPLE_DIR_PROXY
export WEX_SED_I_ORIG_EXT=".orig"    # Used by sed to store a local temp backup file before removing it.
export WEX_WEXAMPLE_DIR_PROXY=$([[ "$(uname -s)" == Darwin ]] && echo /Users/.wex/server/ || echo /opt/wex_server/)    # /opt can't be mounted on macos, using Users instead.
export WEX_WEXAMPLE_DIR_PROXY_TMP=${WEX_WEXAMPLE_DIR_PROXY}tmp/
export WEX_QUIET_MODE='off'
export WEX_QUIET_MODE_PREVIOUS='off'
export WEX_SCREEN_WIDTH=$(tput cols)
export WEX_TRUCATE_SPACE=4 # 3 dots plus one space.

. ${WEX_DIR_BASH}colors.sh

_wexAppDetected() {
  local DIR=$(_wexAppDir)

  if [ "${DIR}" != "" ]; then
    echo true
  else
    echo false
  fi;
}

_wexAppDir() {
  local PATH_CURRENT=${PWD}

  # Saved statically
  if [ "${WEX_APP_DIR}" != "" ]; then
    echo ${WEX_APP_DIR}
    return
  fi;

  while [[ ${PATH_CURRENT} != / ]];
  do
      if [ -f "${PATH_CURRENT}/.wex" ]; then
        WEX_APP_DIR=${PATH_CURRENT}"/"
        echo ${WEX_APP_DIR}
        return
      fi
      PATH_CURRENT=$(dirname ${PATH_CURRENT}"/")
  done
}

_wexAppLoadConfig() {
  if [ "${WEX_APP_DIR}" != "" ]; then
    . ${WEX_APP_DIR}.wex
  fi;
}

_wexAppVersion() {
  # No wex app folder.
  if [ $(_wexAppDetected) == false ];then
    return;
  fi

  local WEX_VERSION=""
  . $(_wexAppDir).wex

  # Treat undefined app as v2
  if [ "${WEX_VERSION}" != "" ];then
    echo ${WEX_VERSION}

  else
    echo ${WEX_VERSION_FALLBACK}
  fi
}

_wexBashCheckVersion() {
  # Check bash version.
  if [ -z ${WEX_BASH_VERSION+x} ]; then
    WEX_BASH_VERSION_MIN='4'
    WEX_BASH_VERSION=$(_wexVersionGetMajor ${BASH_VERSION})
    if [ ${WEX_BASH_VERSION} -lt ${WEX_BASH_VERSION_MIN} ]; then
      _wexError "Wex error, need to run on bash version "${WEX_BASH_VERSION_MIN} "Your current version is ${WEX_BASH_VERSION}"
      exit
    fi;
  fi;
}

_wexError() {
  printf "${WEX_COLOR_RED}[wex] Error : ${1}${WEX_COLOR_RESET}\n"

  # Complementary information or description for extra text
  if [ "${2}" != "" ];then
    printf "      ${WEX_COLOR_CYAN}${2}${WEX_COLOR_RESET}\n"
  fi

  # Extra text
  if [ "${3}" != "" ];then
    printf "      ${3}\n"
  fi
}

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
  export WEX_SCRIPT_METHOD_NAME=$(_wexMethodName ${WEX_SCRIPT_CALL_NAME})
  export WEX_SCRIPT_METHOD_ARGS_NAME=${WEX_SCRIPT_METHOD_NAME}"Args";

  # Use main script if still not exists.
  if [ -f ${WEX_SCRIPT_FILE} ] || [ -d ${WEX_SCRIPT_DIR} ]; then
    export WEX_NAMESPACE=${WEX_NAMESPACE_TEST}
  else
    export WEX_NAMESPACE=${WEX_NAMESPACE_DEFAULT}
    # Search into wexample local folder.
    export WEX_SCRIPT_FILE=${WEX_DIR_BASH}${WEX_NAMESPACE_DEFAULT}/${WEX_SCRIPT_CALL_NAME}.sh
  fi;

  # Load namespace init file.
  . "${WEX_DIR_BASH}${WEX_NAMESPACE}/init.sh"
}

_wexHasRealPath() {
  if [[ $(type -t realpath 2>/dev/null) == file ]];then
    echo "true";
  else
    echo "false";
  fi;
}

_wexItem() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  local ICON="*"
  if [ "${3}" != "" ];then
    ICON=${3}
  fi

  local ICON_COLOR=${WEX_COLOR_GRAY}
  if [ "${4}" != "" ];then
    ICON_COLOR=${4}
  fi

  local TEXT="    ${ICON_COLOR}${ICON}${WEX_COLOR_RESET}    ${1}${WEX_COLOR_RESET}"

  # Complementary information or description for extra text
  if [ "${2}" != "" ];then
    TEXT+="${WEX_COLOR_CYAN}${2}${WEX_COLOR_RESET}"
  fi

  printf "${TEXT}\n"
}

_wexItemFail() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  _wexItem "${@}" "x" "${WEX_COLOR_RED}"
}

_wexItemSuccess() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  _wexItem "${@}" "✓" "${WEX_COLOR_GREEN}"
}

_wexLog() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  local MAX_WIDTH
  # Add wrapper length and regular space.
  MAX_MIDTH=$((${WEX_SCREEN_WIDTH} - 4 - ${WEX_TRUCATE_SPACE}))

  MESSAGE=$(_wexTruncate "${1}" ${MAX_MIDTH})

  printf "${WEX_COLOR_GRAY}  - ${WEX_COLOR_LIGHT_GRAY}${MESSAGE}${WEX_COLOR_RESET}\n"
}

_wexMessage() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  printf "${WEX_COLOR_CYAN}[wex]${WEX_COLOR_RESET} ${1}${WEX_COLOR_RESET}\n"

  # Complementary information or description for extra text
  if [ "${2}" != "" ];then
    printf "      ${WEX_COLOR_CYAN}${2}${WEX_COLOR_RESET}\n"
  fi

  # Extra text
  if [ "${3}" != "" ];then
    printf "      ${3}\n"
  fi
}

_wexMethodName() {
  local SPLIT=(${1//// })
  echo ${SPLIT[0]}$(_wexUpperCaseFirstLetter ${SPLIT[1]})
}

_wexSubTitle() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  printf "${WEX_COLOR_GRAY}##${WEX_COLOR_CYAN} ${1}${WEX_COLOR_RESET}\n"
}

_wexTitle() {
  if [ "${WEX_QUIET_MODE}" = "on" ];then
    return
  fi;

  printf "${WEX_COLOR_GRAY}# ${WEX_COLOR_YELLOW} ${1}${WEX_COLOR_RESET}\n"
}

_wexTruncate() {
  if [ "${#1}" -gt "${2}" ];then
    echo "$(echo "${1}" | cut -c -"${2}")${WEX_COLOR_GRAY}...${WEX_COLOR_RESET} "
    return
  fi

  echo "${1}"
}

_wexUpperCaseFirstLetter() {
  echo $(tr '[:lower:]' '[:upper:]' <<< ${1:0:1})${1:1}
}

_wexVersionGetMajor() {
  sed -n "s/\([[:digit:]]\{0,\}\)\([\.].\{0,\}\)/\1/p" <<< ${1}
}
