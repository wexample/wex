#!/bin/bash

# Remove built in scripts
rm -rf /opt/wexample
# Copy current (let a copy in place for ci tools)
cp -r /builds/wexample-public/scripts /opt/wexample
# Go to
cd /opt/wexample

# Add permission to execute
chmod -R +x "/opt/wexample"
# Load wexample.
. ./project/bash/ubuntu-16.x/_installLocal.sh

# Init gitlab
# We need to install dependencies only for Docker
[[ ! -e /.dockerenv ]] && exit 0

set -xe

# Install global packages
apt-get update -yqq

# Install composer : we use some libraries in PHP scripts
wex composer/pharInstall

# Run all tests
bash bash/ubuntu-16.x/_tests/_run.sh

# Deploy on GitHub
wex wexample::gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
