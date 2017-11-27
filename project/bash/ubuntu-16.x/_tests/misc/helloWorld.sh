#!/usr/bin/env bash

miscHelloWorldVerify() {
  # Test echoed message.
  wexTestAssertEqual "${1}" "Hello World!"
}
