#!/usr/bin/env bash

grafanaConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=grafana"
  echo "\nGRAFANA_VERSION="${GRAFANA_VERSION}
}
