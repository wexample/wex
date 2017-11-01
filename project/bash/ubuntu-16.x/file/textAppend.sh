#!/usr/bin/env bash

fileTextAppendArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
   [1]='line l "New line" true'
 )
}

fileTextAppend() {
  printf "\r\n${LINE}" >> ${FILE}
}
