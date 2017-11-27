#!/usr/bin/env bash

siteInfoArgs() {
  _ARGUMENTS=(
    [0]='no_recreate nr "No recreate if files exists" false'
  )
}

siteInfo() {
  wex site/configWrite
  wex site/configLoad
  SITE_NAME=$(wex site/config -k=name)

  . .env

  echo ""
  echo -e "  Started : \t\t "$(wex site/started)
  echo -e "  Machine name : \t "${SITE_NAME}
#  echo -e "  Framework : \t\t "$(wex framework/detect -d="project")
  echo -e "  Environment : \t "${SITE_ENV}
  echo -e "  Domains : \t\t "$(wex site/domains)

#  wex framework/settings
#  echo ""
#  echo -e "  DB name : \t\t "${SITE_DB_HOST}
#  echo -e "  DB host : \t\t "${SITE_DB_NAME}
#  echo -e "  DB user : \t\t "${SITE_DB_USER}
#  echo -e "  DB password : \t "${SITE_DB_PASSWORD}
#
#  echo ""
#  echo "  Local hosts names :"
#  echo $(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
#  echo ""

  # Compose file may have not been created
  if [[ -f ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML} ]];then
    cat ${WEX_WEXAMPLE_SITE_COMPOSE_BUILD_YML}
  fi
}
