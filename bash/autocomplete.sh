#!/usr/bin/env bash

WEX_DIR_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")/"
WEX_DIR_TMP="${WEX_DIR_ROOT}tmp/"
WEX_DIR_TMP_AUTOCOMPLETE="${WEX_DIR_TMP}cache/autocomplete/"

autocomplete() {
  local CUR=${COMP_WORDS[${COMP_CWORD}]}

  # Avoid empty search.
  if [ "${COMP_CWORD}" = "1" ] && [ "${CUR}" = "" ]; then
    return
  fi

  local SUGGESTIONS=""
  local CHECKSUM=$(echo "${COMP_WORDS[@]}" | md5sum | grep -o '^\S\+')
  local WEX_FILE_CACHE

  local WEX_FILE_CACHE="${WEX_DIR_TMP_AUTOCOMPLETE}${CHECKSUM}"

  if [ -f "${WEX_FILE_CACHE}" ]; then
    SUGGESTIONS=$(cat "${WEX_FILE_CACHE}")
  else
    . "${WEX_DIR_ROOT}includes/globals.sh"

    local CUR_ADDON=""
    local LOCATIONS
    local PART_NAME=""

    if [ "${COMP_WORDS[2]}" == "::" ]; then
      CUR_ADDON=${COMP_WORDS[1]}
      local ADDON_PATH="${WEX_DIR_ADDONS}${COMP_WORDS[1]}/bash/"

      if [ -d "${ADDON_PATH}" ]; then
        LOCATIONS=(${ADDON_PATH})
      fi

      CUR=${COMP_WORDS[3]}

      if ((COMP_CWORD < 4)); then
        PART_NAME="command"
      else
        PART_NAME="args"
      fi
    else
      LOCATIONS=$(_wexFindScriptsLocations)

      if ((COMP_CWORD < 2)); then
        PART_NAME="command"
      else
        PART_NAME="args"
      fi
    fi

    # We are on the "group/name", or addon::group/name, sections.
    if [ "${PART_NAME}" = "command" ]; then
      if [ ! -f "${WEX_DIR_TMP}all-scripts" ];then
        return
      fi

      SUGGESTIONS=$(cat "${WEX_DIR_TMP}all-scripts")
    else
      local WEX_CALLING_ARGUMENTS=()

      _wexGetArguments "${WEX_SCRIPT_CALL_NAME}"

      for ((i = 0; i < ${#WEX_CALLING_ARGUMENTS[@]}; i++)); do
        eval "PARAMS=(${WEX_CALLING_ARGUMENTS[${i}]})"
        local ARG_EXPECTED_LONG=${PARAMS[0]}

        SUGGESTIONS+=" --${ARG_EXPECTED_LONG}"
      done
    fi
  fi

  COMPREPLY=($(compgen -W "${SUGGESTIONS[@]}" -- ${CUR}))
}

autocomplete
