#!/usr/bin/env bash

appTestArgs() {
  _ARGUMENTS=(
    'test_file f "File to test" false'
    'test_method m "Method to test into file" false'
  )
}

appTest() {
  wex hook/exec -c=appTest
}