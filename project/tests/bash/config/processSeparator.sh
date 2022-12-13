#!/usr/bin/env bash

configProcessSeparatorTest() {
  _wexTestAssertEqual "$(wex config/processSeparator -s=XXX)" "\(XXX\)\{1,\}"
}

