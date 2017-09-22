#!/usr/bin/env bash

# Replace a variable name into a config file
bashConfigReplaceSettingName() {
  settingName=$1
  settingNewName=$2
  configFile=$3
  sed -i "s/\($settingName *= *\)/$settingNewName = /" ${configFile}
}
