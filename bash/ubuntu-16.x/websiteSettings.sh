#!/usr/bin/env bash

websiteSettings() {
  # Detect type.
  websiteType=$(wexample websiteFrameworkDetect ${1});
  # Get file path.
  settingsPath=$(wexample websiteFrameworkSettingsPath ${websiteType})
  # Parse file.
  wexample ${websiteType}'Settings' ${1}"/"${settingsPath}
}
