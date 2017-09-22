#!/usr/bin/env bash

WEX_DIR_BASH_UBUNTU16="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../"
WEX_DIR_ROOT=${WEX_DIR_BASH_UBUNTU16}"../../"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"
WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"
WEX_NON_INTERACTIVE=false

declare -A WEX_FRAMEWORKS_SETTINGS_PATHS=(
  ['drupal7']='sites/default/settings.php'
  ['symfony3']='app/config/parameters.yml'
  ['wordpress4']='wp-config.php'
);

# Check bash version.
if [ -z ${WEX_BASH_VERSION+x} ]; then
  WEX_BASH_VERSION=$(sed -n "s/\([[:digit:]]*\)\([\.].*\)/\1/p" <<< ${BASH_VERSION})
  if [ ${WEX_BASH_VERSION} != '4' ]; then
    echo "Wexample error, need to run on bash version ${WEX_BASH_VERSION}"
    exit 1
  fi;
fi;

wexampleMethodName() {
  SPLIT=(${1//// })
  METHOD_NAME=${SPLIT[1]}
  echo ${SPLIT[0]}$(tr '[:lower:]' '[:upper:]' <<< ${METHOD_NAME:0:1})${METHOD_NAME:1}
}

wex() {
  WEX_SHOW_INTRO=false
  WEX_REMOVE_DOWNLOADED_SCRIPT=false
  WEX_SCRIPT_CALL_NAME=${1}

  if [ ${WEX_SCRIPT_CALL_NAME} == "wexample" ];then
    return
  fi;

  # Get parameters keeping quoted strings.
  WEX_ARGUMENTS=''
  whitespace="[[:space:]]"
  for i in "${@:2}"
  do
      if [[ $i =~ $whitespace ]]
      then
          i=\"$i\"
      fi
      WEX_ARGUMENTS=${WEX_ARGUMENTS}' '${i}
  done

  # Check if script is provided.
  if [ "${WEX_SCRIPT_CALL_NAME}" = false ]; then
    echo "You should use a script name, use -s or --script, and provide an existing name.";
    exit 1;
  fi;

  # Check if file exists locally.
  # It allow to override behaviors from location where script is executed,
  # especially for contextual website scripts.
  WEX_SCRIPT_FILE="./../wexample/bash/ubuntu-16.x/${WEX_SCRIPT_CALL_NAME}.sh"
  WEX_SCRIPT_METHOD_NAME=$(wexampleMethodName ${WEX_SCRIPT_CALL_NAME})

  # File does not exists.
  if [ ! -f ${WEX_SCRIPT_FILE} ]; then
    # Search into wexample local folder.
    WEX_SCRIPT_FILE="${WEX_DIR_BASH_UBUNTU16}${WEX_SCRIPT_CALL_NAME}.sh"
  fi;

  # File does not exists.
  if [ ! -f ${WEX_SCRIPT_FILE} ]; then
    echo "Script not found ${WEX_SCRIPT_FILE} > ${WEX_SCRIPT_METHOD_NAME}()"
    exit 1
  fi;

  # Include loaded file
  . "${WEX_SCRIPT_FILE}"

  # Init empty var.
  _ARGUMENTS=()
  # Catch arguments
  ARGS_METHOD=${WEX_SCRIPT_METHOD_NAME}"Args";

  # Execute arguments method
  if [[ $(type -t "${ARGS_METHOD}" 2>/dev/null) == function ]]; then
    # Execute command
    ${ARGS_METHOD}
  fi;

  # Add extra parameters at end of array
  _ARGUMENTS+=(
    'nonInteractive ni "Non interactive mode" false'
    'help h "Help" false'
  )
  # Then start in negative value (length of previous table).
  _NEGATIVE_ARGS_LENGTH=2

  # We iterate first on system extra parameters
  # Using negative values allow to use clean push method on array.
  for ((i=-${_NEGATIVE_ARGS_LENGTH}; i < ${#_ARGUMENTS[@]}-${_NEGATIVE_ARGS_LENGTH}; i++)); do
    eval "PARAMS=(${_ARGUMENTS[${i}]})"
    ARG_EXPECTED_LONG=${PARAMS[0]}
    ARG_EXPECTED_SHORT=${PARAMS[1]}
    eval $(unset ${ARG_EXPECTED_LONG^^})

    FOUND=false

    # Get args given,
    # ignore first one which is always method name.
    for ARG_GIVEN in "${@:2}"
    do
      ARG_GIVEN_NAME=$(sed -e 's/--\?\(.*\)\=.*/\1/' <<< ${ARG_GIVEN})
      ARG_GIVEN_VALUE=$(sed -e 's/--\?.*\=\(.*\)/\1/' <<< ${ARG_GIVEN})

      if [[ ${ARG_GIVEN_NAME} == ${ARG_EXPECTED_LONG} || ${ARG_GIVEN_NAME} == ${ARG_EXPECTED_SHORT} ]]; then
        FOUND=true
        eval ${ARG_EXPECTED_LONG^^}=${ARG_GIVEN_VALUE}
      # Support --noEqualSign -nes
      elif [[ "--"${ARG_EXPECTED_LONG} == ${ARG_GIVEN} || "-"${ARG_EXPECTED_SHORT} == ${ARG_GIVEN} ]]; then
        FOUND=true
        eval ${ARG_EXPECTED_LONG^^}=true
      fi
    done;

    # If an argument is not found
    # And we are not on help page.
    if [ ${FOUND} == false ] && [ -z ${HELP+x} ];then
      # Expected
      if [ ${PARAMS[3]} == true ]; then
        # Interactive mode allowed.
        if [ -z ${NONINTERACTIVE+x} ] || [ ${NONINTERACTIVE} == false ]; then
          echo -n ${PARAMS[2]}": "
          read ${ARG_EXPECTED_LONG^^}
        else
          echo "Error | ${WEX_SCRIPT_METHOD_NAME} | Expected argument not found : "${ARG_EXPECTED_LONG}
          # Raise an error.
          # Unable to fetch expected variable
          exit 0
        fi;
      fi;
    fi;
  done

  # Show help manual
  if [ ! -z ${HELP+x} ]; then
    for ((i=-${_NEGATIVE_ARGS_LENGTH}; i < ${#_ARGUMENTS[@]}-${_NEGATIVE_ARGS_LENGTH}; i++)); do
      eval "PARAMS=(${_ARGUMENTS[${i}]})"
      ARG_EXPECTED_LONG=${PARAMS[0]}
      echo "--"${PARAMS[0]}" -"${PARAMS[1]}
      if [ ${PARAMS[3]} == true ]; then
      echo "                (required)"
      fi;
      echo "                "${PARAMS[2]}
    done;
  else
    # Execute function with all parameters.
    eval ${WEX_SCRIPT_METHOD_NAME} ${WEX_ARGUMENTS}
  fi;

  # Expected since we use read
  exit
}

# Execute run function with same arguments.
# Using false as argument allow to protect unexpected argument passing
if [ ! -z "${1+x}" ] && [ "${1}" != '' ] && [ ${1} != false ]; then
  wex "$@"
fi;
