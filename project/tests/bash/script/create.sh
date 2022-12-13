#!/usr/bin/env bash

scriptCreateTest() {
  local FILEPATH
  FILEPATH=$(wex script/create -s=lorem/ipsum)

  if [ ! -f "${FILEPATH}" ];then
    _wexTestResultError "File must be created ${FILEPATH}"
  else
    _wexTestResultSuccess "File created ${FILEPATH}"
  fi

  _wexTestAssertEqual "$(wex lorem/ipsum)" "Do something."
}
