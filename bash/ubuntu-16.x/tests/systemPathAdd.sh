#!/usr/bin/env bash

systemPathAddTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}bashrc
  newPath=/toto/tata

  command=$(wexample systemPathAdd ${newPath} ${filePath})
  if [ "${command}" == '' ]; then
    wexampleTestError 'Command must not be empty'
  fi

  # Fake added to path (not exported)
  PATH=$PATH":${newPath}"

  # Exactly the same command
  command=$(wexample systemPathAdd ${newPath} ${filePath})
  if [ "${command}" != '' ]; then
    wexampleTestError "Command must be empty (exists), got : ${command}"
  fi

  # Revert
  git checkout HEAD -- ${filePath}
}
