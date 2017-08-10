#!/usr/bin/env bash

wexampleFrameworkDumpLatestPath() {
  . ".env"
  # Get database connexion global settings.
  wexample frameworkSettings ./
  # Get environment from this framework type.
  prefix=$(wexample frameworkGetEnvironment)"-"
  # Build path.
  echo ${VOLUME_DATA_DUMPS}"/"${prefix}${WEBSITE_SETTINGS_DATABASE}"-latest.sql"
}
