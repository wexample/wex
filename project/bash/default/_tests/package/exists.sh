#!/usr/bin/env bash

packageExistsTest() {
  # There is a good chance that bash was installed
  value=$(wex package/exists -n="bash")
  wexTestAssertEqual ${value} true

  value=$(wex package/exists -n="undefinedTestPackage")
  wexTestAssertEqual ${value} false
}
