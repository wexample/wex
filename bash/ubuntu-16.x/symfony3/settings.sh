#!/usr/bin/env bash

symfony3Settings() {
  eval $(php "${WEX_DIR_BASH_UBUNTU16}../../php/symfony3SettingsToBash.php" ${1});
}
