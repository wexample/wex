#!/usr/bin/env bash

monitorConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=monitor"
  echo "\nMONITOR_VERSION="${MONITOR_VERSION}
}
