#!/usr/bin/env bash

_siteInitTest_createSite() {
  SITE_TEST_FOLDER=${1}
  SERVICES=${2}

  # go to temp folder
  cd ${WEX_TEST_DIR_TMP}

  # Folder exists.
  if [[ -d ${SITE_TEST_FOLDER} ]];then
    # Do not create.
    return
  fi

  mkdir ${SITE_TEST_FOLDER}
  cd ${SITE_TEST_FOLDER}

    # Default container name.
  if [ -z ${SERVICES+x} ]; then
    # Get all services separated by a comma
      SERVICES=$(ls ${WEX_DIR_ROOT}"services" | tr "\n" " " )
      SERVICES=$(wex array/join -a="${SERVICES}" -s=",")
  fi

  wexLog "Create test site in "${SITE_TEST_FOLDER}" with "${SERVICES[@]}

  $(wex wexample::site/init -s=${SERVICES}) &> /dev/null

  wex wexample::service/exec -c="test"

  wexLog "Test site created in "${SITE_TEST_FOLDER}

  wexTestAssertEqual $([[ -f .wex ]] && echo true || echo false) true
}

_siteInitTest_checkSitesNumber() {
  _siteInitTest_checkConfLines ${1} "sites"
}

_siteInitTest_checkHostsNumber() {
  _siteInitTest_checkConfLines ${1} "hosts"
}

_siteInitTest_checkConfLines() {
  local FILE_NAME=${2}
  wexLog "Check running ${FILE_NAME} in "${WEX_DIR_PROXY_TMP}
  NUM=${1}

  if [[ -f ${WEX_PROXY_APPS_REGISTRY} ]];then
    # Add an empty line to lines count.
    . ${WEX_DIR_BASH}wexample/init.sh
    COUNT=$(wex file/linesCount -i -f=${WEX_DIR_PROXY_TMP}${FILE_NAME})
  else
    wexLog "Server is stopped (no ${FILE_NAME} file)"
    COUNT=0
  fi

  wexLog "Running ${FILE_NAME} count : "${COUNT}", expected "${NUM}
  wexTestAssertEqual $([[ ${COUNT} == ${NUM} ]] && echo true || echo false) true
}

_siteInitTest_checkRange() {
  wexLog "Checking config "${WEX_APP_CONFIG}
  SITE_TEST_PORT_RANGE_EXPECTED=${1}
  # Load config file
  . ${WEX_APP_CONFIG}
  # Port range is zero
  wexLog "Website port range is "${SITE_PORT_RANGE}", expected "${SITE_TEST_PORT_RANGE_EXPECTED}
  wexTestAssertEqual true $([[ ${SITE_PORT_RANGE} == ${SITE_TEST_PORT_RANGE_EXPECTED} ]] && echo true || echo false)
}
