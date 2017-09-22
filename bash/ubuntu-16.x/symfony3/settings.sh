#!/usr/bin/env bash

symfony3SettingsArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root directory of symfony3" false'
 )
}

symfony3Settings() {
  eval $(php "${WEX_DIR_BASH_UBUNTU16}../../php/symfony3SettingsToBash.php" ${DIR});
}
