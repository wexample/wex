#!/usr/bin/env bash

mysqlDump() {
  websiteDir=./
  dumpDir=./
  prefix=''
  gzip=false

  # Manage arguments
  # https://stackoverflow.com/a/14203146/2057976
  for i in "$@"
  do
    case $i in
        -s=*|--site=*)
        websiteDir="${i#*=}"
        shift # past argument
        ;;
        -d=*|--destination=*)
        dumpDir="${i#*=}"
        shift # past argument
        ;;
        -p=*|--prefix=*)
        prefix="${i#*=}"
        shift # past argument
        ;;
        -gz|--gzip)
        gzip=true
        shift # past argument
        ;;
    esac
  done

  # Get database connexion global settings.
  wexample websiteSettings ${_TEST_RUN_DIR_SAMPLES}${websiteDir}"/"

  # Add -p option only if password is defined and not empty.
  # Adding empty password will prompt user instead.
  if [ "${WEBSITE_SETTINGS_PASSWORD}" != "" ]; then
    WEBSITE_SETTINGS_PASSWORD="-p\"${WEBSITE_SETTINGS_PASSWORD}\""
  fi;

  # Build dump name.
  dumpFullPath=${dumpDir}"/"${prefix}${WEBSITE_SETTINGS_DATABASE}"-"$(wexample dateTimeFileName)".sql"

  # Create dump file
  mysqldump -h${WEBSITE_SETTINGS_HOST} -u${WEBSITE_SETTINGS_USERNAME} ${WEBSITE_SETTINGS_PASSWORD} ${WEBSITE_SETTINGS_DATABASE} > ${dumpFullPath}

  if [[ ${gzip} == true ]]; then
    gzip ${dumpFullPath}
  fi
}
