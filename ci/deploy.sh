#!/bin/bash

bash "shell/ubuntu-16.x/installGit.sh"

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git

bash "shell/ubuntu-16.x/gitlabAddSSH.sh"

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Push on git repo.
git push -u github master
