#!/usr/bin/env bash

fileConvertLinesFormatArgs() {
 _ARGUMENTS=(
   'file f "File" true'
   'format t "Destination format" true'
 )
 _REQUIREMENTS=(
   'mac2unix'
   'unix2dos'
   'unix2mac'
 )
}

# dependency : dos2unix
fileConvertLinesFormat() {
  local FILE_FORMAT_CURRENT
  FILE_FORMAT_CURRENT=$(wex file/getLinesFormat -f="${FILE}")

  # Check if format is already set.
  if [ "${FILE_FORMAT_CURRENT}" = "${FORMAT}" ]; then
    return;
  fi;

  # Convert to unix, first from DOS
  if [ "${FILE_FORMAT_CURRENT}" = 'CRLF' ]; then
    dos2unix -q "${FILE}"
  # Or from mac.
  elif [ "${FILE_FORMAT_CURRENT}" = 'CR' ]; then
    mac2unix -q "${FILE}"
  fi;

  # Convert to final non unix format.
  if [ "${FORMAT}" = "CRLF" ]; then
    unix2dos -q "${FILE}"
  elif [ "${FORMAT}" = 'CR' ]; then
    unix2mac -q "${FILE}"
  fi;
}
