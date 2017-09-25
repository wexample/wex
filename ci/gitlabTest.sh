#!/bin/bash

# Run tests.
bash bash/ubuntu-16.x/tests/_run.sh

wex=bash/ubuntu-16.x/wexample/wexample.sh

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git"
