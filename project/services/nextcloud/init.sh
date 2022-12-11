#!/usr/bin/env bash

nextcloudAppInit() {
  # Override default container.
  echo "NEXTCLOUD_VERSION=18.0.0-apache" >> .wex
}
