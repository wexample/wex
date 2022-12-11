#!/usr/bin/env bash

nextcloudAppInit() {
  # Override default container.
  echo "POSTGRES_VERSION=11.1" >> .wex
}
