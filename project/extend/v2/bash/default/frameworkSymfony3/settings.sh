#!/usr/bin/env bash

frameworkSymfony3SettingsArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of symfony3" true'
  )
}

frameworkSymfony3Settings() {
  eval $(php "${WEX_DIR_ROOT}php/symfony3SettingsToBash.php" ${DIR});
}
