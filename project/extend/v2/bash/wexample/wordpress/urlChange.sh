#!/usr/bin/env bash

wordpressUrlChangeArgs() {
  _ARGUMENTS=(
    [0]='new_url u "New url with trailing slash (ex: http://wexample.com/) " false'
  )
}

wordpressUrlChange() {
  . .wex

  # If no new url defined, use local config.
  if [ "${NEW_URL}" = "" ];then
    . ${WEX_WEXAMPLE_SITE_CONFIG}
    # Do not use https to support local envs.
    NEW_URL="http://${DOMAIN_MAIN}"
  fi

  # Change database records.
  local OLD_URL=$(wex db/exec -c="SELECT option_value FROM ${WP_DB_TABLE_PREFIX}options WHERE option_name = 'siteurl'")

  wex site/exec -l -c="wp search-replace --allow-root ${OLD_URL} ${NEW_URL}"

  # Change wp-config.php
  local NEW_DOMAIN=$(wex domain/fromUrl -u="${NEW_URL}")
  # Protect arguments by escaping special chars.
  NEW_URL=$(sed -e 's/[]\/$\{0,\}.^|[]/\\&/g' <<< "${NEW_DOMAIN}")
  local FILE=./wordpress/config/wp-config.php
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/DOMAIN_CURRENT_SITE/s/'[^']\{0,\}'/'"${NEW_URL}"'/2" ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
}