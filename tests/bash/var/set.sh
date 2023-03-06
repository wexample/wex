#!/usr/bin/env bash

varSetTest() {
  wex-exec var/set -n="testVar" -v="yes man"

  _wexTestAssertEqual "$(wex-exec var/get -n="testVar")" "yes man"
}
