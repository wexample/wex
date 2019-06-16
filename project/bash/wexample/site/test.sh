#!/usr/bin/env bash

siteTest() {
  # For now, only support PHPunit tests.
  wex phpunit/run
}