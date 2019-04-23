#!/usr/bin/env bash

siteTestArgs() {
  _ARGUMENTS=(
    [0]='test_file f "File to test" false'
    [1]='test_method m "Method to test into file" false'
  )
}

siteTest() {
  wex hook/exec -c=siteTest
}