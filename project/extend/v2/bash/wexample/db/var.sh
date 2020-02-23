#!/usr/bin/env bash

dbVarArgs() {
  _ARGUMENTS=(
    [0]='name n "Variable name" true'
  )
}

dbVar() {
  # Load credentials stored into config
  wex config/load
  local NAME='MYSQL_DB_'${ENVIRONMENT^^}
  echo $(eval 'echo ${'${NAME}'}')
}