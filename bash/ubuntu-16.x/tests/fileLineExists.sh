#!/usr/bin/env bash

fileLineExistsTest() {
  filePath=${_TEST_RUN_DIR_SAMPLES}fileTextSample1.txt

  result=$(wexample fileLineExists ${filePath} "Sample text with special chars \ / $ !! ? ;)")
  wexampleTestAssertEqual "${result}" true

  result=$(wexample fileLineExists ${filePath} "[INNER LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wexample fileLineExists ${filePath} "[LAST LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wexample fileLineExists ${filePath} "[FIRST LINE]")
  wexampleTestAssertEqual "${result}" true

  result=$(wexample fileLineExists ${filePath} "[MISSING LINE]")
  wexampleTestAssertEqual "${result}" false

  result=$(wexample fileLineExists ${filePath} ".*")
  wexampleTestAssertEqual "${result}" false
}
