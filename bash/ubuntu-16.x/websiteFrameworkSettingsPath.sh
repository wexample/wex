#!/usr/bin/env bash

websiteFrameworkSettingsPath() {
  declare -A settings=(
    ['drupal7']='sites/default/settings.php'
    ['silex1']='config/config.json'
    ['symfony3']='app/config/parameters.yml'
    ['wordpress4']='wp-config.php'
  );
  echo ${settings[${1}]}
}
