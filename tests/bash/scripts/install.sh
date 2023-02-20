#!/usr/bin/env bash

scriptsInstallTest() {
  _wexTestAssertNotEmpty "$(wex-exec scripts/install --source)"
}
