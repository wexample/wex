#!/usr/bin/env bash

configCommentTest() {
  # Revert file.
  local filePath=$(_wexTestSampleInit configSample)
  local original=$(< ${filePath})

  # Each "uncomment" may not be the exact reversion of "comment" command :
  # It can interact with variables which are already commented at startup
  # So we make initial comment / uncomment test to check the behavior
  # and also verify file integrity.

  # Test with space sign.
  wex-exec default::config/comment -f=${filePath} -k="ConfigTestSingleOption"
  wex-exec default::config/uncomment -f=${filePath} -k="ConfigTestSingleOption"
  _wexTestSampleDiff configSample false "Simple comment / uncomment operation"

  # Values with equal sign after space "example =..." should be also changed.
  wex-exec default::config/comment -f=${filePath} -k="ConfigTestOption"
  _wexTestSampleDiff configSample true "Simple comment"

  wex-exec default::config/uncomment -f=${filePath} -k="ConfigTestOption"
  _wexTestSampleDiff configSample true "Simple uncomment"

  # Revert file.
  filePath=$(_wexTestSampleInit configSample)

  # Test with equal sign
  wex-exec default::config/comment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" -s="="
  wex-exec default::config/uncomment -f=${filePath} -k="ConfigTestSingleOptionWithEqual" -s="="

  _wexTestSampleDiff configSample false "Simple comment / uncomment operation with equal"

  wex-exec default::config/comment -f=${filePath} -k="ConfigTestOptionEqual" -s="="
  _wexTestSampleDiff configSample true "Simple comment with equal"

  # We have uncommented all settings,
  # which are more than original uncommented ones (one and two only)
  wex-exec default::config/uncomment -f=${filePath} -k="ConfigTestOptionEqual" -s="="
  modified=$(< ${filePath})
  # The new value is "four"
  local value=$(wex-exec default::config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s="=")
  _wexTestAssertEqual ${value} "four"
}
