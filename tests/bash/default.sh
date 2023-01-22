#!/usr/bin/env bash

testDefault() {
  # Empty call.
  _wexTestAssertEqual "$(wex)" ""

  _wexTestAssertEqual "$(wex hi)" "hi!"

  _wexTestAssertNotEmpty "$(wex core/logo --help)"

  # Should return an error as test user should ne be sudo
  _wexTestAssertNotEmpty "$(wex scripts/install -d=/home/weeger --non_interactive)"

  # Quiet mode hides errors
  _wexTestAssertEqual "$(wex scripts/install -d=/home/weeger --non_interactive --quiet)" ""
}