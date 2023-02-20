#!/usr/bin/env bash

arrayJoinTest() {
  _wexTestAssertEqual "$(wex-exec array/join -a="a b c")" "abc"

  _wexTestAssertEqual "$(wex-exec array/join -a="a b c" -s=",")" "a,b,c"

  local ARRAY=("a" "b" "c")
  _wexTestAssertEqual "$(wex-exec array/join -a="${ARRAY[*]}" -s=",")" "a,b,c"
}

