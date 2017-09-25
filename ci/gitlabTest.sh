#!/bin/bash

# Run tests.
bash bash/ubuntu-16.x/tests/_run.sh

# Deploy to GitHub
bash $w gitlab/deployGithub "git@github.com:wexample/scripts.git"
