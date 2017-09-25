#!/usr/bin/env bash

fileTextRemoveLastLineArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileTextRemoveLastLine() {
  head -n -1 ${FILE} > ${FILE}.tmp ; mv ${FILE}.tmp ${FILE}
}
