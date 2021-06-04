#!/usr/bin/env bash

wikijsConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=wikijs"
  echo "\nWIKIJS_VERSION="${WIKIJS_VERSION}
}
