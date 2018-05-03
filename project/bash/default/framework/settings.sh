#!/usr/bin/env bash

frameworkSettingsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of framework" false'
  )
}

frameworkSettings() {
  # Detect type.
  websiteType=$(wex framework/detect -d=${DIR});
  if [[ ${websiteType} != 'default' ]];then
    # Get file path.
    settingsPath=$(wex framework/settingsPath -t=${websiteType})
    # Parse file.
    wex "framework"$(wexUpperCaseFirstLetter ${websiteType})'/settings' -d=${DIR}"/"${settingsPath}
  fi;
}
