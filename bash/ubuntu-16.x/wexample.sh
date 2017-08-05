#!/usr/bin/env bash
# @file Contains all needed scripts for wexample
# to get a run given script.

WEX_DIR_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
WEX_URL_GITHUB="https://github.com/wexample/"
WEX_URL_SCRIPTS="https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/"

wexampleIntro() {
  RED='\033[1;91m'
  WHITE='\033[0;30m'
  NC='\033[0m'

  # Continued from above example
  echo -e "${RED}"

  echo "                        .";
  echo "                   .-=======-.";
  echo "               .-=======+=======-.";
  echo "           .-===========++==========-.";
  echo "        .-==========!|==+++|!==========-.";
  echo "        |++=======?  |==!++|  ?=========|";
  echo "        |++++==|     |?   ^|     |======|";
  echo "        |++++++|                 |======|";
  echo "        |++++++|                 |======|";
  echo "        |++++++|                 |======|";
  echo "        |++++++++ _    _!_    _ ========|";
  echo "        ?-+++++++++++.=====.===========-?";
  echo "           ?-+++++++++++============-?";
  echo "               ?-++++++++=======-?";
  echo "                   ?-++++===-?";
  echo "                        +";

  echo -e "${NC}";

  echo "                                          _";
  echo "                                         | |";
  echo "  __      _______  ____ _ _ __ ___  _ __ | | ___";
  echo "  \ \ /\ / / _ \ \/ / _\` | '_ \` _ \| '_ \| |/ _ \\";
  echo "   \ V  V /  __/>  < (_| | | | | | | |_) | |  __/";
  echo "    \_/\_/ \___/_/\_\__,_|_| |_| |_| .__/|_|\___|";
  echo "     http://network.wexample.com   | |";
  echo "     # Scripts recipe              |_|";

  # Extra message is set.
  if [ ! -z "${1+x}" ]; then
    echo "       ~> ${1}";
  fi;
}

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

  if [ "${WEX_SHOW_INTRO}" = true ]; then
    wexampleIntro "${WEX_SCRIPT_NAME}()";
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
      exit 1
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
if [ $# -eq 1 ]; then
  wexample "$@"
fi;
