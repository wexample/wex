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

# Remove branch if exists.
git branch -d temp
# Use temp branch to attach head.
git branch temp
git checkout temp
git branch -f master temp
git checkout master
# Push on git repo.
git push github master
