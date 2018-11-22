#!/usr/bin/env bash

configCommentTest() {

  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  original=$(< ${filePath})

  # Each "uncomment" may not be the exact reversion of "comment" command :
  # It can interact with variables which are already commented at startup
  # So we make initial comment / uncomment test to check the behavior
  # and also verify file integrity.

  # Test with space sign.
  wex config/comment -f=${filePath} -k="ConfigTestSingleOption"
  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOption"

  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))

  if [ "${differences}" != '' ]; then
    wexTestError "Differences found after simple comment / uncomment operation"
  fi

  # Values with equal sign after space "example =..." should be also changed.
  wex config/comment -f=${filePath} -k="ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexTestError "No diff change found after comment test"
  fi

  wex config/uncomment -f=${filePath} -k="ConfigTestOption"
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexTestError "No diff change found after uncomment test"
  fi

  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  # Test with equal sign
  wex config/comment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" -s="="
  wex config/uncomment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" -s="="

  modified=$(< ${filePath})
  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ "${differences}" != '' ]; then
    wexTestError "Differences found after simple comment / uncomment operation with equal"
  fi

  wex config/comment -f=${filePath} -k="ConfigTestOptionEqual" -s="="
  modified=$(< ${filePath})

  differences=$(diff <(echo "${original}") <(echo "${modified}"))
  if [ ${#differences} == 0 ]; then
    wexTestError "No diff change found after comment test"
  fi

  # We have uncommented all settings,
  # which are more than original uncommented ones (one and two only)
  wex config/uncomment -f=${filePath} -k="ConfigTestOptionEqual" -s="="
  modified=$(< ${filePath})
  # The new value is "four"
  local value=$(wex config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s="=")
  wexTestAssertEqual ${value} "four"

}
