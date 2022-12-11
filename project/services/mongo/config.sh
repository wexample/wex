#!/usr/bin/env bash

mongoConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=mongo"
  echo "\nMONGO_VERSION="${MONGO_VERSION}
}
