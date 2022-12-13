#!/usr/bin/env bash

coreLogoTest() {
  _wexTestAssertEqual "$(wex core/logo --quiet)" ""
}
