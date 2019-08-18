#!/usr/bin/env bash

nextcloudInit() {
  # Override default container.
  echo "NEXTCLOUD_VERSION=12.0.7-apache" >> .wex
}
