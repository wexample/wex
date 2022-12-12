#!/usr/bin/env bash

fileTextRemoveLastLineArgs() {
 _ARGUMENTS=(
   'file f "File" true'
 )
}

fileTextRemoveLastLine() {
  head -n -1 "${FILE}" > "${FILE}".tmp ; mv "${FILE}".tmp "${FILE}"
}
