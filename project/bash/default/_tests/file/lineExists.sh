#!/usr/bin/env bash

fileLineExistsTest() {
  filePath=$(wexTestSampleInit "fileTextSample1.txt")

  result=$(wex file/lineExists -f=${filePath} -l="Sample text with special chars \ / $ !! ? ;)")
  wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[INNER LINE]")
  wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[LAST LINE]")
  wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[FIRST LINE]")
  wexTestAssertEqual "${result}" true

  result=$(wex file/lineExists -f=${filePath} -l="[MISSING LINE]")
  wexTestAssertEqual "${result}" false

  result=$(wex file/lineExists -f=${filePath} -l=".*")
  wexTestAssertEqual "${result}" false
}
