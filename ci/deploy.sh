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

# Push on git repo.
git status
git checkout -b github
git checkout -B master github
git push github github
