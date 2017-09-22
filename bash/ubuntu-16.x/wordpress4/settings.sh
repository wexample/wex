#!/usr/bin/env bash

wordpress4SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of wordpress4." false'
 )
}

wordpress4Settings() {
  eval $(php "${WEX_DIR_BASH_UBUNTU16}../../php/wordpress4SettingsToBash.php" ${DIR});
}
