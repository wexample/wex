#!/usr/bin/env bash

gitlabConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=gitlab"
  echo "\nGITLAB_VERSION="${GITLAB_VERSION}
}
