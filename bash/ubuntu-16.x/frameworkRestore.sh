#!/usr/bin/env bash

frameworkRestore() {
  websiteDir=./
  dumpFile=./
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
        -d=*|--dump=*)
        dumpFile="${i#*=}"
        shift # past argument
        ;;
    esac
  done

  # Get database connexion global settings.
  wexample frameworkSettings ${websiteDir}

  # Add -p option only if password is defined and not empty.
  # Adding empty password will prompt user instead.
  if [ "${WEBSITE_SETTINGS_PASSWORD}" != "" ]; then
    WEBSITE_SETTINGS_PASSWORD="-p\"${WEBSITE_SETTINGS_PASSWORD}\""
  fi;

  mysqlConnexion="mysql -h${WEBSITE_SETTINGS_HOST} -u${WEBSITE_SETTINGS_USERNAME} ${WEBSITE_SETTINGS_PASSWORD}"

  # Empty database
  ${mysqlConnexion} -e "DROP DATABASE IF EXISTS ${WEBSITE_SETTINGS_DATABASE}; CREATE DATABASE ${WEBSITE_SETTINGS_DATABASE};"

  # If file is a gzip, gunzip it.
  if [[ ${dumpFile} =~ \.gz$ ]];then
     dumpBaseFile=${dumpFile}
     dumpFile=$(dirname  "${dumpFile%.*}")"/"$(basename  "${dumpFile%.*}")
     gunzip -c ${dumpBaseFile} > ${dumpFile}
  fi;

  # Create dump file
  mysql -h${WEBSITE_SETTINGS_HOST} -u${WEBSITE_SETTINGS_USERNAME} ${WEBSITE_SETTINGS_PASSWORD} ${WEBSITE_SETTINGS_DATABASE} < ${dumpFile}

  # If file was a gzip, .sql file was temporary.
  if [[ ${dumpBaseFile} =~ \.gz$ ]];then
    rm ${dumpFile}
  fi
}
