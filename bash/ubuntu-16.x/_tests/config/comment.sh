#!/usr/bin/env bash

configCommentTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  original=$(< ${filePath})

  # Each "uncomment" may not be the exact reversion of "comment" command :
  # It can interact with variables which are already commented at startup
  # So we make initial comment / uncomment test to check the behavior
  # and also verify file integrity, then we revert file with git.

  # Test with space sign.
  wex config/comment ${filePath} "ConfigTestSingleOption"

  wex config/uncomment ${filePath} "ConfigTestSingleOption"
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation"
    echo ${differences}
  fi

  # Values with equal sign after space "example =..." should be also changed.
  wex config/comment ${filePath} "ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wex config/uncomment ${filePath} "ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi

  # Reset
  git checkout HEAD -- ${filePath}

  # Test with equal sign
  wex config/comment ${filePath} "ConfigTestSingleOptionWithEqual" "="
  wex config/uncomment ${filePath} "ConfigTestSingleOptionWithEqual" "="
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation with equal"
  fi

  wex config/comment ${filePath} "ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wex config/uncomment ${filePath} "ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi
echo "??";
  # Reset
  git checkout HEAD -- ${filePath}
}
