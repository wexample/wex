#!/usr/bin/env bash

watcherStartArgs() {
  _MIGRATED_TO_V3=true
}

watcherStart() {
  wex hook/exec -c=watcherStart
}