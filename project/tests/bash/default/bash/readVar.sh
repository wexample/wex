#!/usr/bin/env bash

bashReadVarTest() {
  _wexTestAssertEqual $(wex bash/readVar -f=${WEX_TEST_RUN_DIR_SAMPLES}configBashSample -k=FIRST_VAR) "first"

  _wexTestAssertEqual $(wex bash/readVar -f=${WEX_TEST_RUN_DIR_SAMPLES}configBashSample -k=NUMBER_VAR) 123
}
