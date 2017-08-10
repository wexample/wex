#!/usr/bin/env bash

phpScriptExecute() {
#  echo $(php ${WEX_DIR_ROOT}"php/"${1});
  echo $(php ${WEX_DIR_ROOT}"php/_execute.php" "$@");
}
