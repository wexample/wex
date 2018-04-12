#!/usr/bin/env bash

systemPathAddTest() {
  filePath=$(wexTestSampleInit bashrc)
  newPath=/toto/tata

  command=$(wex system/pathAdd -p=${newPath} -b=${filePath} -g="Lorem ipsum")
  if [ "${command}" == '' ]; then
    wexTestError 'Command must not be empty'
  fi

  # Exactly the same command with another PATH content
  command=$(wex system/pathAdd -p=${newPath} -b=${filePath} -g="Lorem ipsum:${newPath}")
  if [ "${command}" != '' ]; then
    wexTestError "Command must be empty (exists), got : ${command}"
  fi
}
