#!/usr/bin/env bash

autocomplete() {
  . /opt/wex/project/includes/globals.sh

  local CUR=${COMP_WORDS[${COMP_CWORD}]}
  local LOCATIONS
  local SUGGESTIONS=''
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

  COMPREPLY=( $(compgen -W "${SUGGESTIONS}" -- ${CUR}) )
}

autocomplete