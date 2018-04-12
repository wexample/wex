#!/usr/bin/env bash

_TEST_ARGUMENTS=( '--name=Friend' '-g=Wexample' )

miscHelloWorldArgumentVerify() {
  # Test echoed message.
  wexTestAssertEqual "${1}" "Hello World! - You are Friend from Wexample"
}
