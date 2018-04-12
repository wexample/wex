#!/usr/bin/env bash

gitHookExecArgs() {
  _ARGUMENTS=(
    [0]='name n "Git hook name" true'
  )
}

gitHookExec() {
  local HOOK_SITE_FILE=git/${NAME}
  if [ -f ${HOOK_SITE_FILE} ];then
    . ${HOOK_SITE_FILE}
  fi
}
