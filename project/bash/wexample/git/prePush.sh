#!/usr/bin/env bash

gitPrePush() {
  # FAILURES : A test returned false
  # ERRORS : An error occurred (ex undefined variable)
  RESULT=$(wex site/test)
  # Based on PHPUnit errors, me may move this filter on a more specific script.
  if [[ $(grep -E 'FAILURES|ERRORS' <<< ${RESULT}) != "" ]]; then
    cat <<< ${RESULT}
    echo "Unable to push until tests failed"
    exit 1;
  fi;
}