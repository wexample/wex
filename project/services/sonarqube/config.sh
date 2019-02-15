#!/usr/bin/env bash

sonarqubeConfig() {

  . .wex

  # Set the used version
  echo "\nSONARQUBE_VERSION=${SONARQUBE_VERSION}"
  # Override default container.
  echo "\nSITE_CONTAINER=sonarqube"
}