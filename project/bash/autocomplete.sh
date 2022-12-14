#!/usr/bin/env bash

autocomplete() {
  local CHECKSUM
  local CUR=${COMP_WORDS[${COMP_CWORD}]}
  local WEX_DIR_ROOT
  local WEX_DIR_TMP_AUTOCOMPLETE
  local SUGGESTIONS=''

  CHECKSUM=$(echo "${COMP_WORDS[@]}" | md5sum | grep -o '^\S\+')
  WEX_DIR_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")/"

  WEX_DIR_TMP_AUTOCOMPLETE="${WEX_DIR_ROOT}tmp/cache/autocomplete"
  WEX_FILE_CACHE="${WEX_DIR_TMP_AUTOCOMPLETE}/${CHECKSUM}"

  if [ -f "${WEX_FILE_CACHE}" ];then
    SUGGESTIONS=$(cat "${WEX_FILE_CACHE}")
  else
    . "${WEX_DIR_ROOT}includes/globals.sh"

    local LOCATIONS
    local ARGS_INDEX=2

    LOCATIONS=$(_wexFindScriptsLocations)

    # We are on the "group/name" section.
    if (( COMP_CWORD < ARGS_INDEX ));then
      # Search into extend directories.
      for LOCATION in ${LOCATIONS[@]}
      do
        local SCRIPTS=$(wex scripts/list -d="${LOCATION}")

        for SCRIPT in ${SCRIPTS[@]}
        do
          if [[ "${SCRIPT}" == ${CUR}* ]];then
            SUGGESTIONS+=" ${SCRIPT}"
          fi
        done;
      done;
    # Autocomplete args.
    else
      local WEX_CALLING_ARGUMENTS=()

      _wexGetArguments "${WEX_SCRIPT_CALL_NAME}"

      for ((i=0; i < ${#WEX_CALLING_ARGUMENTS[@]}; i++));
      do
        eval "PARAMS=(${WEX_CALLING_ARGUMENTS[${i}]})"
        local ARG_EXPECTED_LONG=${PARAMS[0]}

        SUGGESTIONS+=" --${ARG_EXPECTED_LONG}"
      done;
    fi

    mkdir -p "${WEX_DIR_TMP_AUTOCOMPLETE}"
    echo "${SUGGESTIONS}" >> "${WEX_FILE_CACHE}"
  fi

  COMPREPLY=( $(compgen -W "${SUGGESTIONS}" -- ${CUR}) )
}

autocomplete
