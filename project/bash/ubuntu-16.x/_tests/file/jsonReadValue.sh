#!/usr/bin/env bash

fileJsonReadValueTest() {
  filePath=$(wexTestSampleInit "jsonSample.json")
  VALUE=$(wex file/jsonReadValue -f=${filePath} -k="simpleValue")
  wexTestAssertEqual "${VALUE}" "value"
}
