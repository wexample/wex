#!/usr/bin/env bash

fileGetLinesFormat() {
  if [[ $(file -b - < ${1}) =~ CRLF ]]; then
    echo "CRLF"
  elif [[ $(file -b - < ${1}) =~ CR ]]; then
    echo "CR"
  else
    echo "LF"
  fi;
}
