#!/usr/bin/env bash

siteConfigArgs() {
 _ARGUMENTS=(
   [0]='key k "Key of config param to get" true'
   [1]='dir d "Root site directory" false'
 )
}

siteConfig() {
  if [ -z "${DIR+x}" ]; then
    DIR=./
  fi;

  echo $(wex file/jsonReadValue -f=${DIR}wex.json -k=${KEY});
}
