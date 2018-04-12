#!/usr/bin/env bash

filesList() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  # Get all files.xxx keys
  wex json/readValue -k="files..*\\" -f=${DIR_SITE}wex.json
}
