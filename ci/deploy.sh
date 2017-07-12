#!/bin/bash

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq

bash shell/ubuntu-16.x/configureSshNoHostCheck.sh

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Install git.
apt-get install git -yqq

# Push on git repo.
git status
git branch -f github master
git checkout github
git push github github
