#!/usr/bin/env bash

siteStartTest() {
  # Stop sites if exists
  $(wex wexample::sites/stop) &>/dev/null

  # Clear dir.
  # wexTestClearTempDir

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  . ${WEX_DIR_BASH}"wexample/_tests/site/_lib.sh"

  # Create a new test site if not exists.
  _siteInitTest_createSite "testsite"

  # Go to fist site
  cd ${WEX_TEST_DIR_TMP}"testsite"

  # Start website
  $(wex site/start) &>/dev/null

  # SERVICES=($(ls ${WEX_DIR_ROOT}"/services" | tr "\n" " " ))
  SERVICES=("web" "mysql" "phpmyadmin") # TODO missing servcies docker files.

  for SERVICE in ${SERVICES[@]};do
    wexLog "Container runs : "${SERVICE}
    wexTestAssertEqual $(wex docker/containerRuns -c="testsite_"${SERVICE}) true
  done

  _siteInitTest_checkRange 0
  # One line
  _siteInitTest_checkSitesNumber 1

  # Start website again
  wexLog "Start first site"
  $(wex site/start) &>/dev/null
  _siteInitTest_checkRange 0
  # One line
  _siteInitTest_checkSitesNumber 1

  # Create a new test site if not exists.
  _siteInitTest_createSite "testsite2"
  # Go to second site
  cd ${WEX_TEST_DIR_TMP}"testsite2"
  # Start second site
  wexLog "Start second site"
  $(wex site/start) &>/dev/null
  _siteInitTest_checkSitesNumber 2
  wexLog "Restart second site"
  $(wex site/restart) &>/dev/null
  _siteInitTest_checkSitesNumber 2

  # Return to fist site
  cd ${WEX_TEST_DIR_TMP}"testsite"
  wexLog "Stop first site"
  $(wex site/stop) &>/dev/null
  _siteInitTest_checkSitesNumber 1

  # Stop all sites
  wexLog "Stop all site (second site should remain)"
  $(wex sites/stop) &>/dev/null
  _siteInitTest_checkSitesNumber 0
}
