#!/usr/bin/env bash

cronReload() {
  if [ ! $(command -v crontab) ];then
    return
  fi

  . .env

  local REGISTRY=$(cat ${WEX_PROXY_APPS_REGISTRY})

  # Copy full crontab in a temp file.
  echo "$(crontab -l)" > ${WEX_DIR_PROXY_TMP}crontab
  # Remove old blocks
  local FILE=${WEX_DIR_PROXY_TMP}crontab
  sed -i"${WEX_SED_I_ORIG_EXT}" -e '/\#\[ wex \]\#/,/\#\[ endwex \]\#/d' ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"

  # Rebuild content.
  echo -e "#[ wex ]#" >> ${WEX_DIR_PROXY_TMP}crontab

  for FILE in ${REGISTRY[@]}
  do
    if [ -f ${FILE}cron/${SITE_ENV} ];then
      echo "# "$(basename ${FILE}) >> ${WEX_DIR_PROXY_TMP}crontab
      cat ${FILE}cron/${SITE_ENV} >> ${WEX_DIR_PROXY_TMP}crontab
    fi
  done;

  echo -e "#[ endwex ]#" >> ${WEX_DIR_PROXY_TMP}crontab

  # Clear crontab
  crontab -r >> /dev/null 2>&1
  # Reset file
  crontab ${WEX_DIR_PROXY_TMP}crontab
  # Remove tmp file
  rm ${WEX_DIR_PROXY_TMP}crontab
}
