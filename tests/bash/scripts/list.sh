#!/usr/bin/env bash

scriptsListTest() {
  _wexTestAssertNotEmpty "$(wex-exec scripts/list -d="${WEX_DIR_BASH}")"

  _wexTestAssertNotEmpty "$(wex-exec scripts/list -d="${WEX_DIR_BASH}" -a="test")"
}
