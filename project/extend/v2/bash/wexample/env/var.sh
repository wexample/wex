#!/usr/bin/env bash

envVarArgs() {
  _ARGUMENTS=(
    [0]='key k "Key to find in env config" true'
    [1]='label l "Description of the variable" false'
    [2]='default d "Default value if not defined" false'
    [3]='ask a "Prompt user if not defined" false'
    [4]='write w "Write new variable in file" false'
  )
}

envVar() {
  # Just wrap method with local env file.
  wex bash/readVar -f=./.env -a="${ASK}" -w="${WRITE}" -l="${LABEL}" -d="${DEFAULT}" -k="${KEY}"
}
