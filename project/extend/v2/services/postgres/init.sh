#!/usr/bin/env bash

nextcloudInit() {
  # Override default container.
  echo "POSTGRES_VERSION=11.1" >> .wex
}
