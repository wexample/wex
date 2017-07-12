#!/usr/bin/env bash

# We need to install dependencies only for Docker
[[ ! -e /.dockerenv ]] && exit 0

set -xe

## Install global packages
apt-get update -yqq





# Install git.
apt-get install git -yqq

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq
mkdir -p ~/.ssh
eval $(ssh-agent -s)
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Push on git repo.
git push -u github master
