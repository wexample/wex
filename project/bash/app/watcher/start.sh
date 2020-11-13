#!/usr/bin/env bash

dbAnonArgs() {
  _DESCRIPTION="Start app watcher for local development"
}

watcherStart() {
  wex hook/exec -c=watcherStart
}