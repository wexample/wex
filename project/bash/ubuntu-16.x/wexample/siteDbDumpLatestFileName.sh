#!/usr/bin/env bash

wexampleSiteDbDumpLatestFileNameArgs() {
 _ARGUMENTS=(
   [0]='dir d "Root site directory" false'
 )
}

wexampleSiteDbDumpLatestFileName() {
  SITE_NAME=$(wex file/jsonReadValue -f=${DIR}wexample/wex.json -k=siteName);
  wex wexample/siteLoadConf -d=${DIR}
  # Get environment from this framework type.
  prefix=${SITE_ENV}"-"
  # Build path.
  echo ${prefix}${SITE_NAME}"-latest.sql"
}
