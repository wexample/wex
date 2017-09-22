#!/usr/bin/env bash

fileExistsArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileExists() {
  [ ! -f ${1} ];
}
