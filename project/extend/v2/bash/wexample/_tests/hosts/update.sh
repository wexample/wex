#!/usr/bin/env bash

hostsUpdateTest() {
  filePath=$(wexTestSampleInit "hosts")

  wexTestAssertEqual true true
}
