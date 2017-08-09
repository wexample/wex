#!/usr/bin/env bash

wordpress4Settings() {
  eval $(php "${WEX_DIR_ROOT}../../php/wordpress4SettingsToBash.php" ${1});
}
