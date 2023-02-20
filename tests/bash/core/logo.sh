#!/usr/bin/env bash

coreLogoTest() {
  _wexTestAssertEqual "$(wex-exec core/logo --quiet)" ""
}
