#!/usr/bin/env bash

laravel5WatcherStart() {
  # TODO Merge with symfony watcher
  local WATCH="yarn watch"

  # Try to use yarn on host if exists,
  # it improve compatibility with editors
  # and performance improvement.
  if [ $(wex package/exists -n=yarn) == true ];then
    cd ./project
    ${WATCH}
  else
    _wexMessage "To improve performance an compatibility you may install yarn to your host machine" "It will be used as file watcher"
    wex site/exec -l -c="${WATCH}"
  fi
}