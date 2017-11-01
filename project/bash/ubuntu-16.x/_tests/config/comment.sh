#!/usr/bin/env bash

configCommentTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  original=$(< ${filePath})

  # Each "uncomment" may not be the exact reversion of "comment" command :
  # It can interact with variables which are already commented at startup
  # So we make initial comment / uncomment test to check the behavior
  # and also verify file integrity, then we revert file with git.

  # Test with space sign.
  wex config/comment -f=${filePath} -k="ConfigTestSingleOption"

  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOption"
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation"
    echo ${differences}
  fi

  # Values with equal sign after space "example =..." should be also changed.
  wex config/comment -f=${filePath} -k="ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wex config/uncomment -f=${filePath} -k="ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi

  # Reset
  git checkout HEAD -- ${filePath}

  # Test with equal sign
  wex config/comment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" "="
  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" "="
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation with equal"
  fi

  wex config/comment -f=${filePath} -k="ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wex config/uncomment -f=${filePath} -k="ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi

  # Reset
  git checkout HEAD -- ${filePath}
}
