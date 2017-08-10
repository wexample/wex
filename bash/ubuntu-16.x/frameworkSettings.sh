#!/usr/bin/env bash

frameworkSettings() {
  # Detect type.
  websiteType=$(wexample frameworkDetect ${1});
  # Get file path.
  settingsPath=$(wexample frameworkSettingsPath ${websiteType})
  # Parse file.
  wexample ${websiteType}'Settings' ${1}"/"${settingsPath}
}
