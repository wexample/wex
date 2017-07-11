#!/bin/bash

wexample_dir="$HOME/"
wexample_url="https://network.wexample.com"

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

# Load common methods.

# This is a general-purpose function to ask Yes/No questions in Bash, either
# with or without a default answer. It keeps repeating the question until it
# gets a valid answer.
# from https://gist.github.com/davejamesmiller/1965569
ask() {
  # http://djm.me/ask
  while true; do

  if [ "${2:-}" = "Y" ]; then
    prompt="Y/n"
    default=Y
  elif [ "${2:-}" = "N" ]; then
    prompt="y/N"
    default=N
  else
    prompt="y/n"
    default=
  fi

  # Ask the question (not using "read -p" as it uses stderr not stdout)
  echo -n "$1 [$prompt] "

  # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
  read REPLY </dev/tty

  # Default?
  if [ -z "$REPLY" ]; then
    REPLY=$default
  fi

  # Check if the reply is valid
  case "$REPLY" in
    Y*|y*) return 0 ;;
    N*|n*) return 1 ;;
  esac

  done
}

# Load given recipe
wexample_load_recipe () {
  script_id=$1
  file_name="wexample-$script_id.sh"
  # Load the file and
  # convert windows lines breaks
  echo "Loading $file_name..."
  sudo curl $wexample_url/node/$script_id/recipe/raw | tr -d "\015" > ${file_name}
  # Run
  echo "Exectue $file_name"
  sudo bash ${file_name}
  # Destroy file
  echo "Remove $file_name"
  sudo rm ${file_name}
}

# Replace a value of a variable into a config file
wexample_replace_config_setting() {
  setting_name=$1
  setting_value=$2
  config_file=$3
  sed -i "s/\($setting_name *= *\).*/\1$setting_value/" ${config_file}
}

# Replace a variable name into a config file
wexample_replace_config_setting_name() {
  setting_name=$1
  setting_new_name=$2
  config_file=$3
  sed -i "s/\($setting_name *= *\)/$setting_new_name = /" ${config_file}
}

# Append a new line to the given
wexample_insert_text_at_end() {
  text=$1
  file_name=$2
  sed -i "\$a$text" ${file_name}
}

echo "Starting wexample recipe : Run wexample script ...............";

# Use standard method to load script
wexample_load_recipe $1

echo "Wexample script complete .....................................";
