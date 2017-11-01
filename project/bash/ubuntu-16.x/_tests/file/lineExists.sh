#!/usr/bin/env bash

fileLineExistsTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt

  result=$(wex file/lineExists -f=${filePath} -l="Sample text with special chars \ / $ !! ? ;)")
  wexampleTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[INNER LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[LAST LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[FIRST LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[MISSING LINE]")
  wexampleTestAssertEqual "${result}" false

  result=$(wex file/lineExists -f=${filePath} -l=".*")
  wexampleTestAssertEqual "${result}" false
}
