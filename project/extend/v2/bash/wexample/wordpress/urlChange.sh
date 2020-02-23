#!/usr/bin/env bash

wordpressUrlChangeArgs() {
  _ARGUMENTS=(
    [0]='new_url u "New url with trailing slash (ex: http://wexample.com/) " true'
  )
}

wordpressUrlChange() {
  . .wex

  # Change database records.
  local OLD_URL=$(wex db/exec -c="SELECT option_value FROM ${WP_DB_TABLE_PREFIX}options WHERE option_name = 'siteurl'")
  local QUERY=''

  QUERY+="UPDATE ${WP_DB_TABLE_PREFIX}options SET option_value = replace(option_value, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${WP_DB_TABLE_PREFIX}posts SET guid = REPLACE (guid, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${WP_DB_TABLE_PREFIX}posts SET post_content = REPLACE (post_content, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${WP_DB_TABLE_PREFIX}posts SET post_excerpt = REPLACE (post_excerpt, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${WP_DB_TABLE_PREFIX}postmeta SET meta_value = REPLACE (meta_value, '${OLD_URL}','${NEW_URL}');"

  wex db/exec -c="${QUERY}"

  # Change wp-config.php
  local NEW_DOMAIN=$(wex domain/fromUrl -u="${NEW_URL}")
  # Protect arguments by escaping special chars.
  NEW_URL=$(sed -e 's/[]\/$\{0,\}.^|[]/\\&/g' <<< "${NEW_DOMAIN}")
  local FILE=./wordpress/config/wp-config.php
  sed -i"${WEX_SED_I_ORIG_EXT}" -e "/DOMAIN_CURRENT_SITE/s/'[^']\{0,\}'/'"${NEW_URL}"'/2" ${FILE}
  rm ${FILE}"${WEX_SED_I_ORIG_EXT}"
}