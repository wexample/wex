#!/usr/bin/env bash

silex1Settings() {
  eval $(php "${WEX_DIR_ROOT}../../php/silex1SettingsToBash.php" ${1} ${2});
}
