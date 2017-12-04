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

_siteInitTest_createSite() {
  SITE_TEST_FOLDER=${1}
  SITE_TEST_PORT_RANGE_EXPECTED=${2}

  # go to temp folder
  cd ${WEX_TEST_DIR_TMP}

  # Folder exists.
  if [[ -d ${SITE_TEST_FOLDER} ]];then
    # Do not create.
    return
  fi

  mkdir ${SITE_TEST_FOLDER}
  cd ${SITE_TEST_FOLDER}

  # Get all services separated by a comma
  SERVICES=$(ls ${WEX_DIR_ROOT}"docker/services" | tr "\n" " " )
  SERVICES=$(wex array/join -a="${SERVICES}" -s=",")

  wexLog "Create test site in "${SITE_TEST_FOLDER}" with "${SERVICES[@]}

  $(wex wexample::site/init -s=${SERVICES}) &> /dev/null

  wex wexample::service/exec -c="test"

  wexLog "Test site created in "${SITE_TEST_FOLDER}

  wexTestAssertEqual $([[ -f wex.json ]] && echo true || echo false) true
}
