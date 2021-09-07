#!/usr/bin/env bash

symfony5WatcherStart() {
  . .env

  # Try to run yarn from outside container for performance purpose.
  if [ "$(wex package/exists -n=yarn)" == "true" ];then
    cd ./project/
    yarn watch
    return;
  fi

  # Fallback inside instead.
  wex site/exec -l -c="yarn watch"
}