#!/bin/bash

mv /builds/wexample-public/scripts /opt/wexample
cd /opt/wexample

ls -la

# Load wexample.
bash bash/ubuntu-16.x/_installLocal.sh

# Init gitlab
wex gitlab/init

# Install composer : we use some libraries in PHP scripts
wex composer/pharInstall

# Run all tests
bash bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
