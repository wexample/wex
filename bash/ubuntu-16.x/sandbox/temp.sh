#!/usr/bin/env bash

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

