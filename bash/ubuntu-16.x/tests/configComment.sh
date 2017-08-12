#!/usr/bin/env bash

configCommentTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}configSample

  original=$(< ${filePath})

  # Each "uncomment" may not be the exact reversion of "comment" command :
  # It can interact with variables which are already commented at startup
  # So we make initial comment / uncomment test to check the behavior
  # and also verify file integrity, then we revert file with git.

  # Test with space sign.
  wexample configComment ${filePath} "ConfigTestSingleOption"
  wexample configUncomment ${filePath} "ConfigTestSingleOption"
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation"
    echo ${differences}
  fi

  # Values with equal sign after space "example =..." should be also changed.
  wexample configComment ${filePath} "ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wexample configUncomment ${filePath} "ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi

  # Reset
  git checkout HEAD -- ${filePath}

  # Test with equal sign
  wexample configComment ${filePath} "ConfigTestSingleOptionWithEqual" "="
  wexample configUncomment ${filePath} "ConfigTestSingleOptionWithEqual" "="
  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [[ ${differences} != '' ]]; then
    wexampleTestError "Differences found after simple comment / uncomment operation with equal"
  fi

  wexample configComment ${filePath} "ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after comment test"
  fi

  wexample configUncomment ${filePath} "ConfigTestOptionEqual" "="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexampleTestError "No diff change found after uncomment test"
  fi

  # Reset
  git checkout HEAD -- ${filePath}
}
