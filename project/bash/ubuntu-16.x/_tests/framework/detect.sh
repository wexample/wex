#!/usr/bin/env bash

frameworkDetectTest() {
  # Silex
  type=$(wex framework/detect -d="${_TEST_RUN_DIR_SAMPLES}silex1")
  wexampleTestAssertEqual ${type} "silex1"
  # Symfony
  type=$(wex framework/detect -d="${_TEST_RUN_DIR_SAMPLES}symfony3")
  wexampleTestAssertEqual ${type} "symfony3"
  # Wordpress
  type=$(wex framework/detect -d="${_TEST_RUN_DIR_SAMPLES}wordpress4")
  wexampleTestAssertEqual ${type} "wordpress4"
  # Drupal
  type=$(wex framework/detect -d="${_TEST_RUN_DIR_SAMPLES}drupal7")
  wexampleTestAssertEqual ${type} "drupal7"
}
