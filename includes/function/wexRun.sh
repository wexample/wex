#!/usr/bin/env bash

wexRun() {
  # Using false as an argument allows to load a file and initialize wex
  # without executing any script.
  if [ -z "${1+x}" ] || [ "${1}" = '' ] || [ ${1} = false ]; then
    return
  fi

  # Running unit test.
  if [ "${1}" = "test" ]; then
    sudo -E bash "${WEX_DIR_BASH}test.sh" "${2}" "${3}"
    return
  fi

  local WEX_SCRIPT_FILE
  local WEX_SCRIPT_METHOD_NAME
  local WEX_SCRIPT_FOUND=false
  local WEX_CALL_SWITCH_SUDO_COMMAND=${WEX_SWITCH_SUDO_COMMAND}

  WEX_SCRIPT_CALL_NAME="${1}"
  # Try constructing path from given name,
  # which is slower.
  WEX_SCRIPT_FILE=$(_wexFindScriptFile "${WEX_SCRIPT_CALL_NAME}")

  if [ ! -f "${WEX_SCRIPT_FILE}" ]; then
    . "${WEX_DIR_ROOT}includes/colors.sh"

    # Show hi
    if [ "${WEX_SCRIPT_CALL_NAME}" = "hi" ]; then
      printf "hi!\n"
    # Not found.
    elif [ ${WEX_SCRIPT_FOUND} = false ]; then
      _wexError "Script not found" "${WEX_SCRIPT_CALL_NAME}"
    fi

    return
  fi

  # Get parameters keeping quoted strings.
  WEX_ARGUMENTS=''
  whitespace="[[:space:]]"
  for i in "${@:2}"; do
    if [[ $i =~ $whitespace ]]; then
      ARG_NAME=$(echo ${i} | cut -d"=" -f1)
      ARG_VALUE=${i#*\=}
      i="-"${ARG_NAME}"=\"${ARG_VALUE}\""
    fi
    WEX_ARGUMENTS+=' '${i}
  done

  WEX_SCRIPT_METHOD_NAME=$(_wexMethodName "${WEX_SCRIPT_CALL_NAME}")

  # Include found script file
  . "${WEX_SCRIPT_FILE}"
  # Disable space as array item separator

  local _AS_SUDO=true
  local _AS_NON_SUDO=true
  local WEX_CALLING_ARGUMENTS=()
  _wexGetArguments "${WEX_SCRIPT_CALL_NAME}"
  local ORIGINAL_ARGS=("${@:2}")

  # Then start in negative value (length of previous table).
  local _NEGATIVE_ARGS_LENGTH="${#WEX_ARGUMENT_DEFAULTS[@]}"
  # We iterate first on system extra parameters
  # Using negative values allow to use clean push method on array.
  for ((i = -_NEGATIVE_ARGS_LENGTH; i < ${#WEX_CALLING_ARGUMENTS[@]} - _NEGATIVE_ARGS_LENGTH; i++)); do
    local WEX_ARG_FOUND=false
    eval "PARAMS=(${WEX_CALLING_ARGUMENTS[${i}]})"
    local ARG_EXPECTED_LONG=${PARAMS[0]}
    local ARG_EXPECTED_SHORT=${PARAMS[1]}
    # Mark variable as empty
    local ${ARG_EXPECTED_LONG^^}=
    # Set it as null.
    eval 'unset '${ARG_EXPECTED_LONG^^}

    # Get args given,
    # ignore first one which is always method name.
    local ARG_SEARCH=0

    for ARG_GIVEN in "${ORIGINAL_ARGS[@]}"; do
      ARG_GIVEN_NAME=$(sed -e 's/-\{1,2\}\([^\=]\{0,\}\)\=.\{0,\}/\1/' <<<${ARG_GIVEN})
      ARG_GIVEN_VALUE=${ARG_GIVEN#*\=}

      if [ "${ARG_GIVEN_NAME}" = "${ARG_EXPECTED_LONG}" ] || [ "${ARG_GIVEN_NAME}" = "${ARG_EXPECTED_SHORT}" ]; then
        WEX_ARG_FOUND=true
        local ${ARG_EXPECTED_LONG^^}="${ARG_GIVEN_VALUE}"
      # Support --noEqualSign -nes
      # Support also space separator.
      elif [ "--${ARG_EXPECTED_LONG}" = "${ARG_GIVEN}" ] || [ "-${ARG_EXPECTED_SHORT}" = "${ARG_GIVEN}" ]; then
        WEX_ARG_FOUND=true
        ARG_SEARCH_NEXT=$((${ARG_SEARCH} + 1))
        ARG_NEXT_VALUE=${ORIGINAL_ARGS[${ARG_SEARCH_NEXT}]}

        # Use next arguments as value if exits
        if [ "${ARG_NEXT_VALUE}" != "" ] && [ "$(echo "${ARG_NEXT_VALUE}" | head -c 1)" != "-" ]; then
          local ${ARG_EXPECTED_LONG^^}="${ARG_NEXT_VALUE}"
          # Ignore next parsing.
          ARG_SEARCH=ARG_SEARCH_NEXT
        else
          local ${ARG_EXPECTED_LONG^^}=true
        fi
      fi

      ((ARG_SEARCH++))
    done

    if [ ! -z ${QUIET+x} ]; then
      # Override all messages and errors functions
      WEX_FILE_MESSAGE_FUNCTION="${WEX_DIR_ROOT}includes/function/messages-quiet.sh"
      . "${WEX_FILE_MESSAGE_FUNCTION}"
    fi

    # If argument not found and not on help page and not in source
    if [ "${WEX_ARG_FOUND}" = "false" ] && [ -z ${HELP+x} ] && [ -z ${SOURCE+x} ]; then
      # If default value is set in arguments list
      if [ "${PARAMS[4]}" != "" ]; then
        local ${ARG_EXPECTED_LONG^^}="${PARAMS[4]}"
      # If expected argument
      elif [ "${PARAMS[3]}" = "true" ]; then
         # If interactive mode is allowed
        if [ -z ${NON_INTERACTIVE+x} ] || [ "${NON_INTERACTIVE}" = "false" ]; then
          printf "${WEX_COLOR_CYAN}${PARAMS[2]}:${WEX_COLOR_RESET} "
          read ${ARG_EXPECTED_LONG^^}
        else
          _wexError "Expected argument not found" "${WEX_SCRIPT_METHOD_NAME} : "${ARG_EXPECTED_LONG}
          # Raise an error: Unable to fetch expected variable
          exit 0
        fi
      fi
    fi
  done

  # Show help manual
  if [ ! -z ${HELP+x} ]; then
    . "${WEX_DIR_ROOT}includes/colors.sh"

    echo ""
    printf '.%.0s' {1..60}
    printf "\n"

    printf "${WEX_COLOR_CYAN}Name${WEX_COLOR_RESET}\t\t${WEX_SCRIPT_CALL_NAME}\n"
    printf "${WEX_COLOR_CYAN}Function${WEX_COLOR_RESET}\t${WEX_SCRIPT_METHOD_NAME}\n"
    printf "${WEX_COLOR_CYAN}File${WEX_COLOR_RESET}\t\t${WEX_SCRIPT_FILE}\n"
    printf "${WEX_COLOR_CYAN}Requirements${WEX_COLOR_RESET}\t${_REQUIREMENTS[*]}\n"

    if [ "${_DESCRIPTION}" != "false" ]; then
      echo ""
      printf "${WEX_COLOR_CYAN}Description${WEX_COLOR_RESET}\n"
      echo "${_DESCRIPTION}" | fold -w 60
    fi

    echo ""
    printf "${WEX_COLOR_CYAN}Arguments${WEX_COLOR_RESET}\n"

    for ((i = -${_NEGATIVE_ARGS_LENGTH}; i < ${#WEX_CALLING_ARGUMENTS[@]} - ${_NEGATIVE_ARGS_LENGTH}; i++)); do
      eval "PARAMS=(${WEX_CALLING_ARGUMENTS[${i}]})"
      ARG_EXPECTED_LONG=${PARAMS[0]}

      TEXT=$(wex text/color -c=lightblue -t="--${PARAMS[0]} -${PARAMS[1]}")

      local PROPS=''

      if [ "${PARAMS[3]}" = "true" ]; then
        PROPS+=[required]
      fi

      if [ "${PARAMS[4]}" != "" ]; then
        PROPS+=[default=\"${PARAMS[4]}\"]
      fi

      if [ "${PROPS}" != "" ]; then
        TEXT+="\n\t$(wex text/color -c=brown -t=${PROPS})"
      fi

      TEXT+="\n\t\t"${PARAMS[2]}
      TEXT+="\n"

      echo -e ${TEXT}
    done

    printf '.%.0s' {1..60}
    echo ""
    echo ""

    return
  # Display script file source.
  elif [ ! -z ${SOURCE+x} ]; then
    . "${WEX_DIR_ROOT}includes/colors.sh"
    printf ${WEX_COLOR_LIGHT_CYAN}
    cat ${WEX_SCRIPT_FILE}
    printf ${WEX_COLOR_RESET}"\n"

    return
  fi

  # User is not sudo.
  if [ "${EUID}" -ne 0 ]; then
    if [ "${_AS_NON_SUDO}" = "false" ]; then
      # User can switch to sudo without password typing
      # Or interactive mode is allowed.
      if [ "$(sudo -n true 2>/dev/null)" = "" ] && [ "${NON_INTERACTIVE}" != "true" ]; then
        # Enforce using sudo
        # Using shorter "wex ${@}" does not pass arguments properly.
        ${WEX_CALL_SWITCH_SUDO_COMMAND} bash -c "wex ${WEX_SCRIPT_CALL_NAME} ${ORIGINAL_ARGS[*]}"
      else
        _wexError "${WEX_SCRIPT_CALL_NAME} should be executed as sudo" "You are \"$(whoami)\", retry with : " "sudo wex ${WEX_SCRIPT_CALL_NAME} ... "
      fi

      return
    fi
  # User is sudo.
  else
    if [ "${_AS_SUDO}" = "false" ]; then
      _wexError "${WEX_SCRIPT_CALL_NAME} should not be executed as sudo" "You are \"$(whoami)\", try to \"exit\" sudo mode, then retry this command"
      return
    fi
  fi

  if [ "${WEX_TRACE_CALLS}" = "true" ];then
    echo "${WEX_SCRIPT_CALL_NAME}" >> "${WEX_FILE_TRACE}"
  fi

  # Execute script with all parameters.
  ${WEX_SCRIPT_METHOD_NAME} "${@:2}"
}
