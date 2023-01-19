#!/usr/bin/env bash

configProcessSeparatorTest() {
  _wexTestAssertEqual "$(wex default::config/processSeparator -s=XXX)" "\(XXX\)\{1,\}"
}

