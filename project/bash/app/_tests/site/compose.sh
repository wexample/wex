#!/usr/bin/env bash

siteComposeTest() {
  . ${WEX_DIR_BASH}"wexample/_tests/site/_lib.sh"

  TEST_SITE_NAME="testsite"

  # Create a new test site if not exists.
  $(_siteInitTest_createSite ${TEST_SITE_NAME}) &> /dev/null

  # Go to test site
  cd ${WEX_TEST_DIR_TMP}${TEST_SITE_NAME}

  RESPONSE=$(wex app/compose -c="config")

  wexTestAssertEqual $([[ ${#RESPONSE} > 10 ]] && echo true || echo false) true
}
