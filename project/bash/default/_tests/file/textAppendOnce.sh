#!/usr/bin/env bash

fileTextAppendOnceTest() {
  filePath=$(wexTestSampleInit fileTextSample1.txt)

  original=$(< ${filePath})

  # Try to append a line which exists
  wex file/textAppendOnce -f=${filePath} -l="[INNER LINE]"
  wexTestSampleDiff fileTextSample1.txt false "Trying insert existing line"

  # Try to append a line which looks like another on but not exactly
  wex file/textAppendOnce -f=${filePath} -l="\n[INNER LINE"
  wexTestSampleDiff fileTextSample1.txt true "Line inserted"

  # Try to append config line
  configValue="true; # With an unsupported comment"
  configKey="SuperConf"
  configTest="${configKey} = ${configValue}"
  wex file/textAppendOnce -f=${filePath} -l="${configTest}"
  inserted=$(wex config/getValue -f=${filePath} -k="${configKey}" -s=" = ")
  wexTestAssertEqual "${inserted}" "${configValue}"

}
