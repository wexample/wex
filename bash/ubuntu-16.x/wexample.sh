#!/usr/bin/env bash

WEX_DIR_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
. "${WEX_DIR_ROOT}/_variables.sh"

wexample() {
  WEX_SHOW_INTRO=false
  WEX_SCRIPT_NAME=false
  WEX_REMOVE_DOWNLOADED_SCRIPT=false
  WEX_SCRIPT_NAME=${1}

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
        -i|--intro)
        WEX_SHOW_INTRO=true
        shift # past argument
        ;;
        -s=*|--script=*)
        WEX_SCRIPT_NAME="${i#*=}"
        shift # past argument
        ;;
        -a=*|--arguments=*)
        WEX_ARGUMENTS="${i#*=}"
        shift # past argument
        ;;
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

  WEX_SCRIPT_FILE="${WEX_DIR_ROOT}${WEX_SCRIPT_NAME}.sh"

  # File does not exists.
  if [ ! -f ${WEX_SCRIPT_FILE} ]; then
    # Load the file and
    # convert windows lines breaks
    echo "Fetching ${WEX_URL_SCRIPTS}${WEX_SCRIPT_NAME}.sh to ${WEX_SCRIPT_FILE}"
    # Cet script content
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
if [ ! -z "${1+x}" ] && [ ${1} != '' ]; then
  wexample "$@"
fi;
