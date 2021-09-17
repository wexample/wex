#!/usr/bin/env bash

grafanaInit() {
  # Override default container.
  echo "GRAFANA_VERSION=master-ubuntu" >> .wex
}
