#!/usr/bin/env bash

siteInitTest() {

  # Empty tmp dir (slower)
  wexTestClearTempDir

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  # Create a site
  _siteInitTest_createSite "testsite"

  # Create a second site
  _siteInitTest_createSite "testsite2"
}
