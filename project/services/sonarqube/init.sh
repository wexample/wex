#!/usr/bin/env bash

sonarqubeAppInit() {
  # Override default container.
  echo "SONARQUBE_VERSION=7.6-community" >> .wex
}
