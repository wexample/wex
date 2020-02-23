#!/usr/bin/env bash

phpExecute() {
  echo $(php ${WEX_DIR_ROOT}"php/_execute.php" "$@");
}
