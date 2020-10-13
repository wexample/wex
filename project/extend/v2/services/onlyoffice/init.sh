#!/usr/bin/env bash

nextcloudInit() {
  # Override default container.
  echo "ONLYOFFICE_DOCUMENT_SERVER_VERSION=5.6" >> .wex
}
