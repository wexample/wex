#!/usr/bin/env bash

envGetVarArgs() {
  _DESCRIPTION="Get env-dependent variable value"
  _ARGUMENTS=(
    'env e "Environment name" false'
    'variable_name n "Variable suffix (prefixed after _, ie VAR_NAME for PROD_VAR_NAME)" true'
  )
}

envGetVar() {
  . .wex

  if [ "${ENV}" = "" ];then
    . .env
    ENV="${SITE_ENV}"
  fi

  eval 'echo ${'${ENV^^}'_'${VARIABLE_NAME^^}'}'
}