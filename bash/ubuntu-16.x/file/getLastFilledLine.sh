#!/usr/bin/env bash

fileGetLastFilledLineArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileGetLastFilledLine() {
  echo $(awk '/./{line=$0} END{print line}' ${FILE})
}
