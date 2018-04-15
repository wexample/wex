#!/usr/bin/env bash

siteLocalVarGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
  )
}

siteLocalVarGet() {
  wex var/localGet -n="${NAME}" -d="${DEFAULT}" -a="${ASK}" -p="${PASSWORD}" -f=./tmp/variablesLocalStorage
}
