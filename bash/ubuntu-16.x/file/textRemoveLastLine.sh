#!/usr/bin/env bash

fileTextRemoveLastLineArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileTextRemoveLastLine() {
  sed -i '$ d' ${FILE}
}
