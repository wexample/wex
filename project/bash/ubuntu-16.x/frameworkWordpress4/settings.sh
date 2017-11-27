#!/usr/bin/env bash

frameworkWordpress4SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of wordpress4" false'
 )
}

frameworkWordpress4Settings() {
  eval $(php "${WEX_DIR_ROOT}php/wordpress4SettingsToBash.php" ${DIR});
}
