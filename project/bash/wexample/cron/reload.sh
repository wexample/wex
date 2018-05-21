#!/usr/bin/env bash

cronReload() {
  . .env

  local REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  local CRONTAB_CURRENT=$(crontab -l)

  if [ "${CRONTAB_CURRENT:0:15}" == "no crontab for " ];then
    CRONTAB_CURRENT=""
  fi

  # Copy full crontab in a temp file.
  echo ${CRONTAB_CURRENT} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
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
  crontab -r
  # Reset file
  crontab ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
  # Remove tmp file
  rm ${WEX_WEXAMPLE_DIR_PROXY_TMP}crontab
}
