#!/usr/bin/env bash

stringTrimTest() {
  _wexTestAssertEqual "$(wex string/trim -s="YES")" "YES"

  _wexTestAssertEqual "$(wex string/trim -s="   YES ")" "YES"

  _wexTestAssertEqual "$(wex string/trim -s="-YES-" -c="-")" "YES"

  _wexTestAssertEqual "$(wex string/trim -s="--YES--" -c="-")" "YES"
}
