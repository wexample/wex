#!/usr/bin/env bash

websiteFrameworkDetectTest() {
  # Silex
  wexample websiteFrameworkDetect "${_TEST_RUN_DIR_SAMPLES}silex1"
  wexampleTestAssertEqual ${WEBSITE_FRAMEWORK} "silex1"
  # Symfony
  wexample websiteFrameworkDetect "${_TEST_RUN_DIR_SAMPLES}symfony3"
  wexampleTestAssertEqual ${WEBSITE_FRAMEWORK} "symfony3"
  # Wordpress
  wexample websiteFrameworkDetect "${_TEST_RUN_DIR_SAMPLES}wordpress4"
  wexampleTestAssertEqual ${WEBSITE_FRAMEWORK} "wordpress4"
  # Drupal
  wexample websiteFrameworkDetect "${_TEST_RUN_DIR_SAMPLES}drupal7"
  wexampleTestAssertEqual ${WEBSITE_FRAMEWORK} "drupal7"
}
