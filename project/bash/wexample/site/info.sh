#!/usr/bin/env bash

siteInfo() {
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wex.json -k=name);

  echo -e "  Machine name : \t "${SITE_NAME}
  echo -e "  Framework : \t\t "$(wex framework/detect -d="project")
}
