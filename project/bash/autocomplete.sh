#!/usr/bin/env bash

autocomplete() {
  local CUR=${COMP_WORDS[${COMP_CWORD}]}

  # Avoid empty search.
  if [ "${COMP_CWORD}" = "1" ] && [ "${CUR}" = "" ]; then
    return
  fi

  local CHECKSUM
  local CUR_ADDON
  local WEX_DIR_ROOT
  local WEX_DIR_TMP_AUTOCOMPLETE
  local WEX_FILE_CACHE
  local SUGGESTIONS=''

  CHECKSUM=$(echo "${COMP_WORDS[@]}" | md5sum | grep -o '^\S\+')
  WEX_DIR_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")/"

  WEX_DIR_TMP_AUTOCOMPLETE="${WEX_DIR_ROOT}tmp/cache/autocomplete"
  WEX_FILE_CACHE="${WEX_DIR_TMP_AUTOCOMPLETE}/${CHECKSUM}"
  WEX_FILE_CACHE=""

  if [ -f "${WEX_FILE_CACHE}" ]; then
    SUGGESTIONS=$(cat "${WEX_FILE_CACHE}")
  else
    . "${WEX_DIR_ROOT}includes/globals.sh"

    local LOCATIONS

    if [ "${COMP_WORDS[2]}" == "::" ]; then
      local ADDON_PATH
      CUR_ADDON=${COMP_WORDS[1]}
      ADDON_PATH="${WEX_DIR_ADDONS}${COMP_WORDS[1]}/bash/"

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
      local ADDON

      # Search into extend directories.
      for LOCATION in ${LOCATIONS[@]}; do
        ADDON=""

        # This is an addon directory.
        if [[ "${LOCATION}" == "${WEX_DIR_ROOT}addons/"* ]]; then
          ADDON=$(basename "$(dirname "${LOCATION}")")
        fi

        local FILTER
        local SCRIPTS
        SCRIPTS=$(wex scripts/list -d="${LOCATION}" -a="${ADDON}")

        for SCRIPT in ${SCRIPTS[@]}; do
          FILTER="${CUR}"
          SUGGESTION="${SCRIPT}"

          if [ "${CUR_ADDON}" != "" ]; then
            FILTER="${CUR_ADDON}::${CUR}"
            SUGGESTION=$(_wexCommandName "${SCRIPT}")
          fi

          if [[ "${SCRIPT}" == ${FILTER}* ]]; then
            SUGGESTIONS+=" ${SUGGESTION}"
          fi
        done
      done
    # Autocomplete args.
    else
      local WEX_CALLING_ARGUMENTS=()

      _wexGetArguments "${WEX_SCRIPT_CALL_NAME}"

      for ((i = 0; i < ${#WEX_CALLING_ARGUMENTS[@]}; i++)); do
        eval "PARAMS=(${WEX_CALLING_ARGUMENTS[${i}]})"
        local ARG_EXPECTED_LONG=${PARAMS[0]}

        SUGGESTIONS+=" --${ARG_EXPECTED_LONG}"
      done
    fi

    #    mkdir -p "${WEX_DIR_TMP_AUTOCOMPLETE}"
    #    echo "${SUGGESTIONS}" >>"${WEX_FILE_CACHE}"
  fi

  COMPREPLY=($(compgen -W "${SUGGESTIONS}" -- ${CUR}))
}

autocomplete
