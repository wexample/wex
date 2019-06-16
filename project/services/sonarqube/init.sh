#!/usr/bin/env bash

sonarqubeInit() {
  # Override default container.
  echo "SONARQUBE_VERSION=7.6-community" >> .wex
}
