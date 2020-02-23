#!/usr/bin/env bash

fileWritableArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileWritable() {
  [ -w ${FILE} ] && echo true || echo false
}