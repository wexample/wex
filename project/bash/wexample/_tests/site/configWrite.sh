#!/usr/bin/env bash

siteConfigWriteTest() {
  . ${WEX_DIR_BASH}"wexample/_tests/site/_lib.sh"

  TEST_SITE_NAME="testsite"

  # Create a new test site if not exists.
  $(_siteInitTest_createSite ${TEST_SITE_NAME}) &> /dev/null

  # Go to test site
  cd ${WEX_TEST_DIR_TMP}testsite

  wex site/configWrite

  wexTestAssertEqual true  $([[ -f "./tmp/config" ]] && echo true || echo false)
  wexTestAssertEqual true  $([[ -f "./tmp/docker-compose.build.yml" ]] && echo true || echo false)

  . ${WEX_WEXAMPLE_SITE_CONFIG}

  wexTestAssertEqual true  $([[ ${TEST_SITE_NAME} == ${SITE_NAME} ]] && echo true || echo false)
}
