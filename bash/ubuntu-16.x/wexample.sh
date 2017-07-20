#!/usr/bin/env bash

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

read_if_missing () {
  variable_name=$1
  message=$2
  if [ -z ${variable_name+x} ]; then echo "var is unset"; else echo "var is set to '$var'"; fi
  read -p "${message} : " host
}

# Load given recipe
wexample_load_recipe () {
  script_id=$1
  file_name="wexample-$script_id.sh"
  # Load the file and
  # convert windows lines breaks
  echo "Loading $file_name..."
  curl $wexample_url/node/$script_id/recipe/raw | tr -d "\015" > ${file_name}
  # Run
  echo "Exectue $file_name"
  bash ${file_name}
  # Destroy file
  echo "Remove $file_name"
  rm ${file_name}
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
