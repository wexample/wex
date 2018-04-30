#!/usr/bin/env bash

# Replace a value of a variable into a config file
bashConfigReplaceSetting() {
  setting_name=$1
  setting_value=$2
  config_file=$3
  sed -i "s/\($setting_name *= *\).*/\1$setting_value/" ${config_file}
}
