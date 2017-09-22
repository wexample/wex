#!/usr/bin/env bash

frameworkSettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of framework." false'
 )
}

frameworkSettings() {
  # Detect type.
  websiteType=$(wex framework/detect -d=${DIR});
  # Get file path.
  settingsPath=$(wex framework/settingsPath -t=${websiteType})
  # Parse file.
  wex ${websiteType}'/settings' -d=${DIR}"/"${settingsPath}
}
