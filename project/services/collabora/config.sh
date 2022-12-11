#!/usr/bin/env bash

collaboraConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=collabora"
  echo "\nCOLLABORA_VERSION="${COLLABORA_VERSION}
}
