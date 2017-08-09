#!/usr/bin/env bash

# Variables are stored globally like
# WEBSITE_SETTINGS_USERNAME,
# WEBSITE_SETTINGS_XXX, etc.
drupal7Settings() {
  eval $(php "${WEX_DIR_ROOT}../../php/drupal7SettingsToBash.php" ${1});
}
