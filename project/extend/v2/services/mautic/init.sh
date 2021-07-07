#!/usr/bin/env bash

mauticInit() {
  # Override default container.
  echo "MAUTIC_VERSION=v3-apache" >> .wex
}
