#!/usr/bin/env bash

dirCountLinesArgs() {
  _ARGUMENTS=(
    [0]='dir d "Directory name" true'
    [1]='extension e "Extension" true'
  )
}

dirCountLines() {
  find ${DIR} -name '*.'${EXTENSION} | xargs wc -l
}