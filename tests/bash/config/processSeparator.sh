#!/usr/bin/env bash

configProcessSeparatorTest() {
  _wexTestAssertEqual "$(wex-exec default::config/processSeparator -s=XXX)" "\(XXX\)\{1,\}"
}

