#!/usr/bin/env bash

WEX_DIR_BASH_UBUNTU16="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
WEX_DIR_ROOT=${WEX_DIR_BASH_UBUNTU16}"../../"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"
WEX_LOCAL_DIR="/opt/wexample/"
WEX_SCRIPTS_DIR=${WEX_LOCAL_DIR}"bash/ubuntu-16.x/"
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

wexample() {
  WEX_SHOW_INTRO=false
  WEX_SCRIPT_NAME=false
  WEX_REMOVE_DOWNLOADED_SCRIPT=false
  WEX_SCRIPT_NAME=${1}

  if [ ${WEX_SCRIPT_NAME} == "wexample" ];then
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

  # Manage arguments
  # https://stackoverflow.com/a/14203146/2057976
  for i in "$@"
  do
    case $i in
        # TODO Avoid arguments propagation, using -wexRm
        -rm|--remove)
        WEX_REMOVE_DOWNLOADED_SCRIPT=true
        shift # past argument
        ;;
    esac
  done

  # Check is script is provided.
  if [ "${WEX_SCRIPT_NAME}" = false ]; then
    echo "You should use a script name, use -s or --script, and provide an existing name.";
    exit 1;
  fi;

  # Check if file exists locally.
  # It allow to override behaviors from location where script is executed,
  # especially for contextual website scripts
  WEX_SCRIPT_FILE="./wexample/bash/ubuntu-16.x/${WEX_SCRIPT_NAME}.sh"

  # File does not exists.
  if [ ! -f ${WEX_SCRIPT_FILE} ]; then
    # Search into wexample local folder.
    WEX_SCRIPT_FILE="${WEX_DIR_BASH_UBUNTU16}${WEX_SCRIPT_NAME}.sh"
  fi;

  # File does not exists.
  if [ ! -f ${WEX_SCRIPT_FILE} ]; then
    # Search file remotely.
    # TODO Place script into local folder if installed.
    # Load the file and
    # convert windows lines breaks
    echo "Fetching ${WEX_URL_SCRIPTS}${WEX_SCRIPT_NAME}.sh to ${WEX_SCRIPT_FILE}"
    # Get script content
    WEX_SCRIPT_CONTENT=$(curl -sS "${WEX_URL_SCRIPTS}${WEX_SCRIPT_NAME}.sh" | tr -d "\015")

    if [ "${WEX_SCRIPT_CONTENT}" == "404: Not Found" ]; then
      echo "The script \"${WEX_SCRIPT_NAME}\" was not found on the remote server."
      return
    else
      # Paste content into script file.
      echo "${WEX_SCRIPT_CONTENT}" > ${WEX_SCRIPT_FILE}
    fi
  fi

  # Include loaded file
  . "${WEX_SCRIPT_FILE}"

  # Execute function with all parameters.
   eval ${WEX_SCRIPT_NAME} ${WEX_ARGUMENTS}

  if [ ${WEX_REMOVE_DOWNLOADED_SCRIPT} == true ]; then
    rm -rf ${WEX_SCRIPT_FILE}
  fi
}

# Execute run function with same arguments.
# Using false as argument allow to protect unexpected argument passing
if [ ! -z "${1+x}" ] && [ ${1} != '' ] && [ ${1} != false ]; then
  wexample "$@"
fi;
