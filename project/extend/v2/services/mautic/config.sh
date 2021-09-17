#!/usr/bin/env bash

mauticConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=mautic"
  echo "\nMAUTIC_VERSION="${MAUTIC_VERSION}
}
