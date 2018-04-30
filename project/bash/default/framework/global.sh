#!/usr/bin/env bash

frameworkGlobal() {
  declare -A -g WEX_FRAMEWORKS_SUPPORTED=(
    ['composer1']='Composer1'
    ['drupal7']='drupal7'
    ['symfony3']='symfony3'
    ['wordpress4']='wordpress4'
  )
  declare -A -g WEX_FRAMEWORKS_SETTINGS_PATHS=(
    ['drupal7']='sites/default/settings.php'
    ['symfony3']='app/config/parameters.yml'
    ['wordpress4']='wp-config.php'
  )
}