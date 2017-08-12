#!/usr/bin/env bash

fileConvertLinesFormat() {
  FILE=${1}
  FORMAT=${2}

  fileFormatCurrent=$(wexample fileGetLinesFormat ${FILE})

  # Check if format is already set.
  if [ ${fileFormatCurrent} == ${FORMAT} ]; then
    return;
  fi;

  # Convert to unix, first from DOS
  if [ ${fileFormatCurrent} == 'CRLF' ]; then
    dos2unix -q ${FILE}
  # Or from mac.
  elif [ ${fileFormatCurrent} == 'CR' ]; then
    mac2unix -q ${FILE}
  fi;

  # Convert to final non unix format.
  if [ ${FORMAT} == "CRLF" ]; then
    unix2dos -q ${FILE}
  elif [ ${FORMAT} == 'CR' ]; then
    unix2mac -q ${FILE}
  fi;
}
