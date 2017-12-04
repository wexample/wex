#!/usr/bin/env bash

siteStartTest() {
  # Stop sites if exists
  $(wex wexample::server/stopSites) &>/dev/null

  # Clear dir.
  # wexTestClearTempDir

  # Load useful variables.
  . ${WEX_DIR_BASH}wexample/init.sh

  . ${WEX_DIR_BASH}"wexample/_tests/site/init.sh"

  # Create a new test site if not exists.
  _siteInitTest_createSite "testsite"

  # Go to fist site
  cd ${WEX_TEST_DIR_TMP}"testsite"

  # Start website
  $(wex site/start) &>/dev/null

  # SERVICES=($(ls ${WEX_DIR_ROOT}"docker/services" | tr "\n" " " ))
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
  $(wex server/stopSites) &>/dev/null
  _siteInitTest_checkSitesNumber 0
}

_siteInitTest_checkSitesNumber() {
  wexLog "Check running websites in "${WEX_WEXAMPLE_DIR_PROXY_TMP}
  NUM=${1}
  # Add an empty line to lines count.
  NUM=$((NUM+1))
  . ${WEX_DIR_BASH}wexample/init.sh
  COUNT=$(wex file/linesCount -f=${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  wexLog "Running websites count : "${COUNT}", expected "${NUM}
  wexTestAssertEqual $([[ ${COUNT} == ${NUM} ]] && echo true || echo false) true
}

_siteInitTest_checkRange() {
  wexLog "Checking config "${WEX_WEXAMPLE_SITE_CONFIG}
  SITE_TEST_PORT_RANGE_EXPECTED=${1}
  # Load config file
  . ${WEX_WEXAMPLE_SITE_CONFIG}
  # Port range is zero
  wexLog "Website port range is "${SITE_PORT_RANGE}", expected "${SITE_TEST_PORT_RANGE_EXPECTED}
  wexTestAssertEqual true $([[ ${SITE_PORT_RANGE} == ${SITE_TEST_PORT_RANGE_EXPECTED} ]] && echo true || echo false)
}

