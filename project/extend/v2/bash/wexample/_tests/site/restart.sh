#!/usr/bin/env bash

siteRestartTest() {

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  . ${WEX_DIR_BASH}"wexample/_tests/site/_lib.sh"

  # Clear dir.
  wexTestClearTempDir
  # Create a new test site if not exists.
  _siteInitTest_createSite "testsite" "web"
  _siteInitTest_createSite "testsite2" "web"
  _siteInitTest_createSite "testsite3" "web"

  wex wexample::server/stop
  wex docker/stopAll

  wex wexample::server/start

  _siteInitTest_checkSitesNumber 1

  cd ${WEX_TEST_DIR_TMP}testsite
  wex site/start
  _siteInitTest_checkSitesNumber 2
  _siteInitTest_checkHostsNumber 1

  cd ${WEX_TEST_DIR_TMP}testsite2
  wex site/start
  _siteInitTest_checkSitesNumber 3
  _siteInitTest_checkHostsNumber 2

  cd ${WEX_TEST_DIR_TMP}testsite3
  wex site/start
  _siteInitTest_checkSitesNumber 4
  _siteInitTest_checkHostsNumber 3

  cd ${WEX_TEST_DIR_TMP}testsite
  wex site/stop
  _siteInitTest_checkSitesNumber 3
  _siteInitTest_checkHostsNumber 2

  cd ${WEX_TEST_DIR_TMP}testsite2
  wex site/stop
  _siteInitTest_checkSitesNumber 2
  _siteInitTest_checkHostsNumber 1

  cd ${WEX_TEST_DIR_TMP}testsite3
  wex site/stop
  _siteInitTest_checkSitesNumber 1
  _siteInitTest_checkHostsNumber 0

}