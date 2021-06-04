#!/usr/bin/env bash

postgresInit() {
  # Override default container.
  echo "POSTGRES_VERSION=13.3" >> .wex
}
