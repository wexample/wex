#!/usr/bin/env bash

dbVarArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
  )
}

dbVar() {
  # Load credentials stored into config
  wex site/configLoad
  local NAME='SITE_DB_'$(wex text/uppercase -t=${NAME})
  echo $(eval 'echo ${'${NAME}'}')
}