#!/usr/bin/env bash

dbPullArgs() {
  _ARGUMENTS=(
    [0]='dump d "Dump to transfer from local" false'
    [1]='environment e "Environment to transfer to" true'
  )
}

dbPull() {
  # Dump must exists in remote server
  if [ -z ${DUMP+x} ];then
    # Show dumps available
    wex wexample::ssh/exec -e=${ENVIRONMENT} -s="wex db/dumpChooseList"
    # Let user choose
    wex wexample::ssh/exec -e=${ENVIRONMENT} -s="wex db/dumpChoose"
  fi
  # Transfer
  wex wexample::file/download -f=./dumps/${DUMP} -d=./dumps/ -e=${ENVIRONMENT}
}
