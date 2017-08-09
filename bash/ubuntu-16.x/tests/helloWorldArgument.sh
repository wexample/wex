#!/usr/bin/env bash

_TEST_ARGUMENTS=( 'Wexample' 'Friends' )

helloWorldArgumentVerify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World! - Wexample - Friends"
}
