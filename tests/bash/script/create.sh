#!/usr/bin/env bash

scriptCreateTest() {
  local FILEPATH
  _wexLog "Creating custom lorem ipsum script..."

  FILEPATH=$(wex script/create -s=lorem/ipsum --quiet)

  if [ ! -f "${FILEPATH}" ];then
    _wexTestResultError "File must be created ${FILEPATH}"
  else
    _wexTestResultSuccess "File created ${FILEPATH}"
  fi

  _wexTestAssertEqual "$(wex lorem/ipsum)" "Do something."
}
