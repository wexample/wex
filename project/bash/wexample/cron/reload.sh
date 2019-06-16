#!/usr/bin/env bash

cronReload() {
  if [ ! $(command -v crontab) ];then
    return
  fi

  . .env

  local REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)

  # Copy full crontab in a temp file.
  echo "$(crontab -l)" > ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
  # Remove old blocks
  sed -i '/\#\[ wex \]\#/,/\#\[ endwex \]\#/d' ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab

  # Rebuild content.
  echo -e "#[ wex ]#" >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab

  for FILE in ${REGISTRY[@]}
  do
    if [ -f ${FILE}cron/${SITE_ENV} ];then
      echo "# "$(basename ${FILE}) >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
      cat ${FILE}cron/${SITE_ENV} >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
    fi
  done;

  echo -e "#[ endwex ]#" >> ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab

  # Clear crontab
  crontab -r >> /dev/null 2>&1
  # Reset file
  crontab ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
  # Remove tmp file
  rm ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
}
