#!/usr/bin/env bash

envReadVarArgs() {
  _ARGUMENTS=(
    [0]='key k "Key to find in env config" true'
    [2]='label l "Description of the variable" false'
    [4]='default d "Default value if not defined" false'
  )
}

envReadVar() {
  wex bash/readVar -f=./.env --ask -w -l=${LABEL} -d=${DEFAULT} -k=${KEY}
}
