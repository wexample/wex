#!/usr/bin/env bash

nextcloudInit() {
  # Override default container.
  echo "NEXTCLOUD_VERSION=18.0.0-apache" >> .wex
}
