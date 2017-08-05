#!/usr/bin/env bash

_TEST_ARGUMENTS=( 'Wexample' 'Friends' )

verify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World! - Wexample - Friends"
}
