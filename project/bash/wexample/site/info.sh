#!/usr/bin/env bash

siteInfo() {
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wex.json -k=name);

  echo ""
  echo -e "  Machine name : \t "${SITE_NAME}
  echo -e "  Framework : \t\t "$(wex framework/detect -d="project")

  wex framework/settings
  echo ""
  echo -e "  DB name : \t\t "${SITE_DB_HOST}
  echo -e "  DB host : \t\t "${SITE_DB_NAME}
  echo -e "  DB user : \t\t "${SITE_DB_USER}
  echo -e "  DB password : \t "${SITE_DB_PASSWORD}

  echo ""

  # Show docker config
  wex site/compose -c="config"
}
