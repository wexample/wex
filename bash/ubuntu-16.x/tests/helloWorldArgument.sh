#!/usr/bin/env bash

arguments() {
  arguments=( 'Wexample' 'Friends' )
}

verify() {
  # Test echoed message.
  wexampleTestAssertEqual "${1}" "Hello World! - Wexample - Friends"
}
