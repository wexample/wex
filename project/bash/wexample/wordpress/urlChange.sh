#!/usr/bin/env bash

wordpressUrlChangeArgs() {
  _ARGUMENTS=(
    [0]='new_url u "New url with trailing slash" true'
    [1]='prefix p "Database prefix" true'
  )
}

wordpressUrlChange() {
  # Change database records.
  local OLD_URL=$(wex db/exec -c="SELECT option_value FROM ${PREFIX}options WHERE option_name = 'siteurl'")
  local QUERY=''

  QUERY+="UPDATE ${PREFIX}options SET option_value = replace(option_value, '${OLD_URL}', '${NEW_URL}') WHERE option_name = 'home' OR option_name = 'siteurl';"
  QUERY+="UPDATE ${PREFIX}posts SET guid = REPLACE (guid, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${PREFIX}posts SET post_content = REPLACE (post_content, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${PREFIX}posts SET post_excerpt = REPLACE (post_excerpt, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE ${PREFIX}postmeta SET meta_value = REPLACE (meta_value, '${OLD_URL}','${NEW_URL}');"

  wex db/exec -c="${QUERY}"

  # Change wp-config.php
  local NEW_DOMAIN=$(wex domain/fromUrl -u="${NEW_URL}")
  # Protect arguments by escaping special chars.
  NEW_URL=$(sed -e 's/[]\/$*.^|[]/\\&/g' <<< "${NEW_DOMAIN}")
  sed -i "/DOMAIN_CURRENT_SITE/s/'[^']*'/'"${NEW_URL}"'/2" ./wordpress/wp-config.php
}