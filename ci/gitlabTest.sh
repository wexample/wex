#!/bin/bash

# Load wexample.
. bash/wex

# Init gitlab
wex gitlab/init

# Install composer : we use some libraries in PHP scripts
wex composer/pharInstall

# Run all tests
bash /opt/wexample/bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
