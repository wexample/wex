#!/usr/bin/env bash

siteStarted() {
  # Get site name.
  CONTAINERS=$(wex site/containers)
  CONTAINERS=$(wex array/join -a="${CONTAINERS}" -s=",")
  wex docker/containerStarted -n="${CONTAINERS}"
}
