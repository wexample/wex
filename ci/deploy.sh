#!/bin/bash

bash "shell/ubuntu-16.x/installGit.sh"

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git

bash "shell/ubuntu-16.x/gitlabAddSSH.sh"

# Push on git repo.
git push -u github master
