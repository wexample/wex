#!/usr/bin/env bash

wordpressUrlChangeArgs() {
  _ARGUMENTS=(
    'new_url n "New url with trailing slash (ex: http://wexample.com/) " false'
    'old_url o "Old url with trailing slash (ex: http://wexample.com/) " false'
  )
}

wordpressUrlChange() {
  . .wex

  # If no new url defined, use local config.
  if [ "${NEW_URL}" = "" ];then
    . ${WEX_APP_CONFIG}
    # Do not use https to support local envs.
    NEW_URL="http://${DOMAIN_MAIN}"
  fi

  if [ "${OLD_URL}" = "" ];then
    # Change database records.
    local OLD_URL=$(wex db/exec -c="SELECT option_value FROM ${WP_DB_TABLE_PREFIX}options WHERE option_name = 'siteurl'")
  fi

  _wexLog "Search / Replace ${OLD_URL} by ${NEW_URL}"

  local TABLES
  local PREFIX_LENGTH
  PREFIX_LENGTH=( ${#WP_DB_TABLE_PREFIX} + 1 )
  TABLES=($(wex db/exec -c="SHOW TABLES"))

  for TABLE in ${TABLES[*]}
  do
    # Remove prefix as it is appeded after
    TABLE=${TABLE:${PREFIX_LENGTH}}
    wex wordpress/urlChangeInTable -t="${TABLE}" -o="${OLD_URL}" -n="${NEW_URL}"
  done

  # Change wp-config.php
  local NEW_DOMAIN=$(wex domain/fromUrl -u="${NEW_URL}")

  _wexLog "Update wp-config.php with ${NEW_URL}"
  # Protect arguments by escaping special chars.
  NEW_URL=$(sed -e 's/[]\/$\{0,\}.^|[]/\\&/g' <<< "${NEW_DOMAIN}")
  local FILE=./wordpress/config/wp-config.php
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/DOMAIN_CURRENT_SITE/s/'[^']\{0,\}'/'"${NEW_URL}"'/2" ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
}