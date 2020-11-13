#!/usr/bin/env bash

dbGo() {
  # Find db type
  local DB_TYPE=$(wex db/detect)
  # Go.
  wex ${DB_TYPE}/go
}
