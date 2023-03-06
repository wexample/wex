#!/usr/bin/env bash

varClearTest() {
  wex-exec var/set -n="testVar" -v="yes man"
  wex-exec var/clear -n="testVar"

  _wexTestAssertEqual "$(wex-exec var/get -n="testVar")" ""
}
