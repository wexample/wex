#!/usr/bin/env bash

stringTrimTest() {
  _wexTestAssertEqual "$(wex-exec string/trim -s="YES")" "YES"

  _wexTestAssertEqual "$(wex-exec string/trim -s="   YES ")" "YES"

  _wexTestAssertEqual "$(wex-exec string/trim -s="-YES-" -c="-")" "YES"

  _wexTestAssertEqual "$(wex-exec string/trim -s="--YES--" -c="-")" "YES"
}
