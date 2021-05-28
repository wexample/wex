#!/usr/bin/env bash

monitorInit() {
  # Override default container.
  echo "N8N_VERSION=nightly" >> .wex
}
