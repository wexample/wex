#!/usr/bin/env bash

jsonReadValueTest() {
  filePath=$(wexTestSampleInit "jsonSample.json")
  VALUE=$(wex json/readValue -f=${filePath} -k="simpleValue")
  wexTestAssertEqual "${VALUE}" "value"
}
