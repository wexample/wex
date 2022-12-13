#!/usr/bin/env bash

scriptsRequirementsTest() {
  _wexTestAssertNotEmpty "$(wex scripts/requirements -d="${WEX_DIR_BASH}")"
}
