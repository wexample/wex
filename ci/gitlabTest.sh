#!/bin/bash

# Run tests.
bash bash/ubuntu-16.x/_tests/_run.sh

# Load wexample.
bash bash/ubuntu-16.x/wexample/wexample.sh

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
