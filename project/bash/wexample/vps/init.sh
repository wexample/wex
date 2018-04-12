#!/usr/bin/env bash

# Install base configuration on a server managed by wexample.
vpsInit() {
  apt-get install git dos2unix -yqq
  # Install docker.
  wex docker/install
  # Disable root login
  wex rootLogin/disable
}
