#!/usr/bin/env bash

nocodbInit() {
  # Override default container.
  echo "NOCODB_VERSION=0.9.41" >> .wex
}
