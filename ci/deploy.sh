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
. ./project/bash/ubuntu-16.x/_installLocal.sh

# Init gitlab
# We need to install dependencies only for Docker
# [[ ! -e /.dockerenv ]] && exit 0

# set -xe

# Install global packages
# apt-get update -yqq

# Install composer : we use some libraries in PHP scripts
# wex composer/pharInstall

# Run all tests
# bash ./project/bash/ubuntu-16.x/_tests/_run.sh

# Generate a version.
VERSION=$(wex version/generate -v=2)

# Add tag if not exists.
echo "Tagging at version "${VERSION}
if [ $(wex git/tagExists -t=${VERSION}) == false ];then
  # Create a tag.
  git tag ${VERSION}
fi;

# Deploy on GitHub
wex wexample::gitlab/deployGithub -r="git@github.com:wexample/scripts.git"

# TODO Rebuild images with username / password of a wexample specific account.
wex wexample::images/rebuild # -d -u=${DOCKER_HUB_USERNAME} -p=${DOCKER_HUB_PASSWORD}
