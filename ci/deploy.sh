#!/usr/bin/env bash

# Install git.
apt-get install git -yqq

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git

# Push on git repo.
git push -u github master
