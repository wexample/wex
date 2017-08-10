#!/usr/bin/env bash

wordpress4Settings() {
  eval $(php "${WEX_DIR_BASH_UBUNTU16}../../php/wordpress4SettingsToBash.php" ${1});
}
