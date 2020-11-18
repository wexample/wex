#!/usr/bin/env bash

systemPathAddTest() {
  newPath=/toto/tata

  filePath=$(wexTestSampleInit bashrc)
  command=$(wex system/pathAdd -p=${newPath} -b=${filePath} -g="Lorem ipsum")
  wexTestSampleDiff bashrc true "Command added to test bashrc file"

  if [ "${command}" == '' ]; then
    wexTestError 'Command must not be empty'
  fi

  filePath=$(wexTestSampleInit bashrc)
  # Exactly the same command with another PATH content
  command=$(wex system/pathAdd -p=${newPath} -b=${filePath} -g="Lorem ipsum:${newPath}")
  wexTestSampleDiff bashrc true "Second command added to test bashrc file"
  if [ "${command}" != '' ]; then
    wexTestError "Command must be empty (exists), got : ${command}"
  fi
}
