#!/usr/bin/env bash

siteInitTest() {

  # Create a site
  _siteInitTest_createSite "testsite" 0

  return
  # One line with an empty line
  _siteInitTest_checkSitesNumber 2

  # Create a second site
  _siteInitTest_createSite "testsite2" 1
  # One more line
  _siteInitTest_checkSitesNumber 3

  # Go to fist site
  cd ${WEX_TEST_DIR_TMP}"testsite"
  # Restart it
  wex site/restart
  _siteInitTest_checkSitesNumber 3
  # Range is still 0
  _siteInitTest_checkRange 0
  wex site/stop
  _siteInitTest_checkSitesNumber 2

  # Go to second site
  cd ${WEX_TEST_DIR_TMP}"testsite2"
  # Restart it
  wex site/restart
  _siteInitTest_checkSitesNumber 2
  # Range changed from 1 to zero.
  _siteInitTest_checkRange 0
  wex site/stop
  _siteInitTest_checkSitesNumber 1
}

_siteInitTest_createSite() {
  SITE_TEST_FOLDER=${1}
  SITE_TEST_PORT_RANGE_EXPECTED=${2}

  # go to temp folder
  cd ${WEX_TEST_DIR_TMP}
  mkdir ${SITE_TEST_FOLDER}
  cd ${SITE_TEST_FOLDER}

  # Get all services separated by a comma
  SERVICES=$(ls ${WEX_DIR_ROOT}"docker/services" | tr "\n" " " )
  SERVICES=$(wex array/join -a="${SERVICES}" -s=",")

  wex wexample::site/init -s=${SERVICES}

return
  # MySQL
  wexTestAssertEqual $(wex file/lineExists -f=".gitignore" -l="/dumps") true

  # Start website
  wex site/start
  _siteInitTest_checkRange ${SITE_TEST_PORT_RANGE_EXPECTED}

  # Start website again
  wex site/start
  _siteInitTest_checkRange ${SITE_TEST_PORT_RANGE_EXPECTED}

  # TODO test domains

  wex server/stopSites

  # TODO server>sites /hosts must be empty
}

_siteInitTest_checkRange() {
  SITE_TEST_PORT_RANGE_EXPECTED=${1}
  # Load config file
  . tmp/config
  # Port range is zero
  wexTestAssertEqual true $([[ ${SITE_PORT_RANGE} == ${SITE_TEST_PORT_RANGE_EXPECTED} ]] && echo true || echo false)
}

_siteInitTest_checkSitesNumber() {
  wexTestAssertEqual true $([[ $(wex file/linesCount -f=${WEX_WEXAMPLE_DIR_PROXY_TMP}sites) == ${1} ]] && echo true || echo false)
}
