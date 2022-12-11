#!/usr/bin/env bash

prometheusInit() {
  # Override default container.
  echo "PROMETHEUS_VERSION=v2.30.0" >> .wex
}
