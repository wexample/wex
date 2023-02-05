#!/usr/bin/env bash

WEX_ADDONS=(app docker language prompt rw services-db services-php services-various system)
WEX_BASHRC_PATH=~/.bashrc
WEX_DIR_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")/"
WEX_DIR_BASH="${WEX_DIR_ROOT}bash/"
WEX_DIR_ADDONS="${WEX_DIR_ROOT}addons/"
WEX_DIR_TMP=${WEX_DIR_ROOT}tmp/
WEX_FILE_MESSAGE_FUNCTION="${WEX_DIR_ROOT}/includes/function/messages.sh"
WEX_SCREEN_WIDTH=$([ "${TERM}" != "unknown" ] && tput cols || echo 100)
WEX_TMP_GLOBAL_VAR=${WEX_DIR_TMP}globalVariablesLocalStorage
WEX_QUIET_MODE=false
WEX_DEFAULT_INSECURE_PASSWORD="thisIsAReallyNotSecurePassword!"

WEX_ARGUMENT_DEFAULTS=(
  'non_interactive non_i "Non interactive mode, use default value in place to ask user\n\t\tIf an argument is missing to not automatically ask for it, but exit." false'
  'help help "Display this help manual" false'
  'debug debug "Show extra debug information, depending of method features" false'
  'source source "Show script source instead to execute it" false'
  'quiet quiet "Hide logs and errors" false'
)

. "${WEX_DIR_ROOT}/includes/colors.sh"
. "${WEX_DIR_ROOT}/includes/function/common.sh"
. "${WEX_FILE_MESSAGE_FUNCTION}"

# Get the username of the original user
if [ "$(_wexUserIsSudo)" = "false" ];then
  WEX_RUNNER_USERNAME=$(whoami)
  WEX_RUNNER_BASHRC_PATH=${WEX_BASHRC_PATH}
  WEX_RUNNER_PATH_HOME=$(realpath ~)/
  WEX_RUNNER_PATH_WEX=${WEX_RUNNER_PATH_HOME}.wex/
  WEX_RUNNER_PATH_BASH=${WEX_RUNNER_PATH_WEX}bash/
fi

WEX_SWITCH_ARGS="WEX_QUIET_MODE=${WEX_QUIET_MODE} \
WEX_RUNNER_USERNAME=${WEX_RUNNER_USERNAME} \
WEX_RUNNER_BASHRC_PATH=${WEX_RUNNER_BASHRC_PATH} \
WEX_RUNNER_PATH_HOME=${WEX_RUNNER_PATH_HOME} \
WEX_RUNNER_PATH_WEX=${WEX_RUNNER_PATH_WEX} \
WEX_RUNNER_PATH_BASH=${WEX_RUNNER_PATH_WEX}"

# Use it to enforce sudo with only useful vars.
WEX_SWITCH_SUDO_COMMAND="sudo ${WEX_SWITCH_ARGS}"
WEX_SWITCH_NON_SUDO_COMMAND="sudo -u ${WEX_RUNNER_USERNAME} ${WEX_SWITCH_ARGS}"
WEX_CHOWN_NON_SUDO_COMMAND="sudo chown ${WEX_RUNNER_USERNAME}:${WEX_RUNNER_USERNAME}"

export WEX_BASHRC_PATH
export WEX_CORE_VERSION=4.0.0
export WEX_DIR_BASH
export WEX_DIR_ROOT
export WEX_DIR_TMP
export WEX_SCREEN_WIDTH
export WEX_SED_I_ORIG_EXT=.orig
export WEX_RUNNER_BASHRC_PATH
export WEX_RUNNER_PATH_HOME
export WEX_RUNNER_PATH_WEX
export WEX_RUNNER_USERNAME
export WEX_SWITCH_SUDO_COMMAND
export WEX_TMP_GLOBAL_VAR

case "$(uname -s)" in
  Darwin)
    WEX_OS='mac'
    ;;
  Linux)
    WEX_OS='linux'
    ;;
  CYGWIN*|MINGW32*|MINGW64*|MSYS*)
    WEX_OS='windows'
    ;;
  # Add here more strings to compare
  # See correspondence table at the bottom of this answer
  *)
    WEX_OS='other OS'
    ;;
esac

# Load addons global files.
for ADDON in "${WEX_ADDONS[@]}"; do
  ADDON_FILE="${WEX_DIR_ADDONS}${ADDON}/includes/globals.sh"

  if [ -f "${ADDON_FILE}" ];then
   . "${ADDON_FILE}";
  fi
done;

# Load addons functions files.
for ADDON in "${WEX_ADDONS[@]}"; do
  ADDON_FILE="${WEX_DIR_ADDONS}${ADDON}/bash/init.sh"

  if [ -f "${ADDON_FILE}" ]; then
   . "${ADDON_FILE}"
  fi
done
