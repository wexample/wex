#!/usr/bin/env bash

sonarqubeConfig() {

  . .wex

  # Set the default supported version
  echo "\nSONARQUBE_VERSION=7.6-community"
  # Override default container.
  echo "\nSITE_CONTAINER=sonarqube"
}