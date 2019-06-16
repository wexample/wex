#!/usr/bin/env bash

gitlabInit() {
  # Override default container.
  echo "GITLAB_VERSION=10.7.2-ce.0" >> .wex
}
