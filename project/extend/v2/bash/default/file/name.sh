#!/usr/bin/env bash

fileNameArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileName() {
  echo "${FILE%.*}"
}