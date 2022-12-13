#!/usr/bin/env bash

coreVersionTest() {
  _wexTestAssertNotEmpty "$(wex core/version)"
}
