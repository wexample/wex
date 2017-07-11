#!/usr/bin/env bash

# We need to install dependencies only for Docker
[[ ! -e /.dockerenv ]] && exit 0

set -xe

## Install global packages
apt-get update -yqq

# 63 is the test script ID.
sh "shell/ubuntu-16.x/wexampleLoader.sh" 63
