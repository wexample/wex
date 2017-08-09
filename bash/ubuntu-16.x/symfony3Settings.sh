#!/usr/bin/env bash

symfony3Settings() {
  eval $(php "${WEX_DIR_ROOT}../../php/symfony3SettingsToBash.php" ${1});
}
