#!/usr/bin/env bash

fileWritableArgs() {
 _ARGUMENTS=(
   'file f "File" true'
 )
}

fileWritable() {
  [ -w "${FILE}" ] && echo true || echo false
}