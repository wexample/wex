#!/usr/bin/env bash

configGetValueTest() {
  # Revert file.
  filePath=$(wexTestSampleInit configSample)

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOption")
  # Got the last valid value
  wexTestAssertEqual "${value}" "two"

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s=" = ")
  wexTestAssertEqual "${value}" "one"

  value=$(wex config/getValue -f=${filePath} -k="ConfigTestOptionEqual" -s="=")
  # Got the last valid value
  wexTestAssertEqual "${value}" "two"
}
