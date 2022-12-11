#!/usr/bin/env bash

dbPushArgs() {
  _ARGUMENTS=(
    [0]='dump d "Dump to transfer from local" false'
    [1]='environment e "Environment to transfer to" true'
  )
}

dbPush() {
  if [ -z ${DUMP+x} ];then
    # Ask user to choose a file.
    wex db/dumpChoiceList
    # Prompt does not work in the exec terminal.
    DUMP=$(wex db/dumpChoose)
  fi
  # Transfer
  wex wexample::file/upload -f=./mysql/dumps/${DUMP} -d=./mysql/dumps/ -e=${ENVIRONMENT}
}
