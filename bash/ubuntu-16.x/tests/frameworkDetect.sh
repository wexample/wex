#!/usr/bin/env bash

frameworkDetectTest() {
  # Silex
  type=$(wexample frameworkDetect "${_TEST_RUN_DIR_SAMPLES}silex1")
  wexampleTestAssertEqual ${type} "silex1"
  # Symfony
  type=$(wexample frameworkDetect "${_TEST_RUN_DIR_SAMPLES}symfony3")
  wexampleTestAssertEqual ${type} "symfony3"
  # Wordpress
  type=$(wexample frameworkDetect "${_TEST_RUN_DIR_SAMPLES}wordpress4")
  wexampleTestAssertEqual ${type} "wordpress4"
  # Drupal
  type=$(wexample frameworkDetect "${_TEST_RUN_DIR_SAMPLES}drupal7")
  wexampleTestAssertEqual ${type} "drupal7"
}
