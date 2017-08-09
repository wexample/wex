#!/usr/bin/env bash

helloWorldVerify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World!"
}
