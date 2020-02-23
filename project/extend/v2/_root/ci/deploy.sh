#!/bin/bash

# Remove built in scripts
rm -rf /opt/wexample
# Copy current (let a copy in place for ci tools)
cp -r /builds/wexample-public/scripts /opt/wexample
# Go to
cd /opt/wexample

# Add permission to execute
chmod -R +x "/opt/wexample"
# Install wexample.
. ./project/bash/default/_installLocal.sh

# Init gitlab
# We need to install dependencies only for Docker
# [[ ! -e /.dockerenv ]] && exit 0

# set -xe

# Install global packages
# apt-get update -yqq

# Install composer : we use some libraries in PHP scripts
# wex composer/pharInstall

# Run all tests
# bash ./project/bash/default/_tests/_run.sh
