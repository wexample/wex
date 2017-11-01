#!/usr/bin/env bash

miscHelloWorldVerify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World!"
}
