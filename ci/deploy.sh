#!/bin/bash

# Add SSH and prevent host checking.
apt-get install openssh-client -yqq

# Same script for multiple sub scripts
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

bash $w -s=sshRemoveHostChecking -rm

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Install git.
apt-get install git -yqq

# Deploy on Github
bash $w -s=gitlabDeployGithub -a="git@github.com:wexample/scripts.git" -rm

# Remove wexample.sh
rm -rf $w
