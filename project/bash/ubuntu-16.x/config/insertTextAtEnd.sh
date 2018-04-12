#!/usr/bin/env bash

# Append a new line to the given file.
# TODO Update to last syntax
bashConfigInsertTextAtEnd() {
  text=$1
  fileName=$2
  sed -i "\$a$text" ${fileName}
}
