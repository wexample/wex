#!/usr/bin/env bash

siteRestartTest() {
  # Clear dir.
  wexTestClearTempDir

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  . ${WEX_DIR_BASH}"wexample/_tests/site/init.sh"

  # Create a new test site if not exists.
  _siteInitTest_createSite "testsite" "web"
  #_siteInitTest_createSite "testsite2" "web"
  #_siteInitTest_createSite "testsite3" "web"
}