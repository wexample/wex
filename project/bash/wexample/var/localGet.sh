#!/usr/bin/env bash

varLocalGetArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
    [1]='default d "Default value" false'
    [2]='ask a "Message to ask user to, enable prompt if provided" false'
    [3]='password p "Hide typed response when asking user" false'
    [4]='required r "Ask again if empty" false'
  )
}

varLocalGet() {
  wex ubuntu-16.x::var/localGet ${WEX_ARGUMENTS} -f=./tmp/variablesLocalStorage
}
