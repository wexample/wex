#!/usr/bin/env bash

dirCountLinesArgs() {
  _ARGUMENTS=(
    'dir d "Directory name" true'
    'extension e "Extension" true'
  )
}

dirCountLines() {
  find "${DIR}" -name "*.${EXTENSION}" | xargs wc -l
}