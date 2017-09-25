#!/bin/bash

# Load wexample.
bash bash/ubuntu-16.x/wexample/wexample.sh

# Init gitlab
wex gitlab/init

# Install composer : we use some libraries in PHP scripts
wex composer/pharInstall

# Run all tests
wexTest

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
