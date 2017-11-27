#!/usr/bin/env bash

frameworkDetectTest() {
  # Silex
  type=$(wex framework/detect -d="${WEX_TEST_RUN_DIR_SAMPLES}silex1")
  wexTestAssertEqual ${type} "silex1"
  # Symfony
  type=$(wex framework/detect -d="${WEX_TEST_RUN_DIR_SAMPLES}symfony3")
  wexTestAssertEqual ${type} "symfony3"
  # Wordpress
  type=$(wex framework/detect -d="${WEX_TEST_RUN_DIR_SAMPLES}wordpress4")
  wexTestAssertEqual ${type} "wordpress4"
  # Drupal
  type=$(wex framework/detect -d="${WEX_TEST_RUN_DIR_SAMPLES}drupal7")
  wexTestAssertEqual ${type} "drupal7"
}
