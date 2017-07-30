#!/bin/bash

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq

# Wexample loader for multiple scripts.
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

# Remove warning on new SSH host.
bash $w -s=sshRemoveHostChecking -rm

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Install git.
apt-get install git -yqq

# Add git repo.
git remote remove github
git remote add github git@github.com:wexample/scripts.git
# Remove branch if exists.
git branch -d temp
# Use temp branch to attach head.
git branch temp
git checkout temp
git branch -f master temp
git checkout master
# Push on git repo.
git push github master
