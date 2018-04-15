#!/usr/bin/env bash

siteLocalVarSetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='value v "Variable value" true'
  )
}

siteLocalVarSet() {
  wex var/localSet -n="${NAME}" -v="${VALUE}" -f=./tmp/variablesLocalStorage
}
