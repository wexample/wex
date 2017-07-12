#!/bin/bash

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq
mkdir -p ~/.ssh
eval $(ssh-agent -s)
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Install git.
apt-get install git -yqq

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git

# Push on git repo.
git add -A
git push -u github master
