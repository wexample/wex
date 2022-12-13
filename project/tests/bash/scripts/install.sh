#!/usr/bin/env bash

scriptsInstallTest() {
  _wexTestAssertNotEmpty "$(wex scripts/install --source)"
}
