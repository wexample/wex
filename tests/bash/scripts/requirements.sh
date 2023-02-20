#!/usr/bin/env bash

scriptsRequirementsTest() {
  _wexTestAssertNotEmpty "$(wex-exec scripts/requirements -d="${WEX_DIR_BASH}")"
}
