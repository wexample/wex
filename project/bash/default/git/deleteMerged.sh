#!/usr/bin/env bash

gitDeleteMergedArgs() {
  _DESCRIPTION="Delete all merged branches except master and develop"
  _ARGUMENTS=(
    'exclude e "Branch to keep even it was merged" true "master|develop"'
  )
}

gitDeleteMerged() {
  local BRANCHES=$(wex git/deletable -e="${EXCLUDE}")

  if [ "${BRANCHES}" != "" ];then
    echo "${BRANCHES}" | xargs git branch -d
  else
    _wexLog "All merged branches has been deleted"
  fi
}
