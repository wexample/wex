#!/usr/bin/env bash

verify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World!"
}
