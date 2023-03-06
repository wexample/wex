#!/usr/bin/env bash

varGetTest() {
  wex-exec var/set -n="testVar" -v="yes"

  _wexTestAssertEqual "$(wex-exec var/get -n="testVar")" "yes"

  _wexTestAssertEqual "$(wex-exec var/get -n="testVarMissing")" ""
}
