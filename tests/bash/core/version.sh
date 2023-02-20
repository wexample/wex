#!/usr/bin/env bash

coreVersionTest() {
  _wexTestAssertNotEmpty "$(wex-exec core/version)"
}
