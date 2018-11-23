#!/usr/bin/env bash

siteInitTest() {

  . ${WEX_DIR_BASH}"wexample/_tests/site/_lib.sh"

  # Empty tmp dir (slower)
  wexTestClearTempDir

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  # Create a site
  _siteInitTest_createSite "testsite"

  # Create a second site
  _siteInitTest_createSite "testsite2"
}
