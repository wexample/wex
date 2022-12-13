#!/usr/bin/env bash

scriptsListTest() {
  _wexTestAssertNotEmpty "$(wex scripts/list -d="${WEX_DIR_BASH}")"
}
