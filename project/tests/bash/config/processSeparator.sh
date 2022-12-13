#!/usr/bin/env bash

processSeparatorTest() {
  _wexTestAssertEqual "$(wex config/processSeparator -s=XXX)" "\(XXX\)\{1,\}"
}

