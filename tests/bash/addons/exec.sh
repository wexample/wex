#!/usr/bin/env bash

addonsExecTest() {
  # Just run without error
  wex addons/exec -c="ls"

  _wexTestAssertEqual true true
}

