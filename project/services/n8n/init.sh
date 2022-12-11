#!/usr/bin/env bash

n8nInit() {
  # Override default container.
  echo "N8N_VERSION=nightly" >> .wex
}
