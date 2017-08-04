#!/usr/bin/env bash

fileTextAppend() {
  text=$1
  file_name=$2
  sed -i "\$a$text" ${file_name}
}
