#!/usr/bin/env bash

packageExistsTest() {
  # There is a good chance that bash was installed
  value=$(wex package/exists -n="bash")
  wexampleTestAssertEqual ${value} true

  value=$(wex package/exists -n="undefinedTestPackage")
  wexampleTestAssertEqual ${value} false
}
