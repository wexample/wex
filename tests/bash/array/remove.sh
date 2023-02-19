#!/usr/bin/env bash

arrayRemoveTest() {
  _wexTestAssertEqual "$(wex array/remove -a="aa bb cc" -i=bb)" "aa cc"
}
