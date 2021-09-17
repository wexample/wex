#!/usr/bin/env bash

nocodbConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=nocodb"
  echo "\nNOCODB_VERSION="${NOCODB_VERSION}
}
