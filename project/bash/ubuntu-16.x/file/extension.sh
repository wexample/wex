#!/usr/bin/env bash

fileExtensionArgs() {
 _ARGUMENTS=(
   [0]='file f "File" true'
 )
}

fileExtension() {
  echo "${FILE##*.}"
}