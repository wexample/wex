#!/usr/bin/env bash

# Append a new line to the given file.
bashConfigInsertTextAtEnd() {
  text=$1
  fileName=$2
  sed -i "\$a$text" ${fileName}
}
