#!/usr/bin/env bash

wordpressUrlChangeArgs() {
  _ARGUMENTS=(
    [0]='new_url u "New url" true'
  )
}

wordpressUrlChange() {
  local OLD_URL=$(wex db/exec -c="SELECT option_value FROM options WHERE option_name = 'siteurl'")
  #local OLD_DOMAIN=$(wex domain/fromUrl -u="${URL}")
  local QUERY=''

  QUERY+="UPDATE options SET option_value = replace(option_value, '${OLD_URL}', '${NEW_URL}') WHERE option_name = 'home' OR option_name = 'siteurl';"
  QUERY+="UPDATE posts SET guid = REPLACE (guid, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE posts SET post_content = REPLACE (post_content, '${OLD_URL}', '${NEW_URL}');"
  QUERY+="UPDATE postmeta SET meta_value = REPLACE (meta_value, '${OLD_URL}','${NEW_URL}');"

  wex db/exec -c="${QUERY}"
}