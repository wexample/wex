#!/usr/bin/env bash

frameworkComposer1UsedArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of framework" false'
  )
}

frameworkComposer1Used() {
  # Search composer file.
  [ $(wex file/exists -f=${DIR}composer.json) == true ] && echo true || echo false
}
