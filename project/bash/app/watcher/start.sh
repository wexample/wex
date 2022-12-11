#!/usr/bin/env bash

watcherStartArgs() {
  _DESCRIPTION="Start app watcher for local development"
}

watcherStart() {
  wex hook/exec -c=watcherStart
}