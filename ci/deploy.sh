#!/bin/bash

# Install required packages
apt-get install openssh-client git curl -yqq

# Same script for multiple sub scripts
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

# Remove warning on new SSH host.
bash $w -s=sshRemoveHostChecking -rm

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Deploy on Github.
bash $w -s=gitlabDeployGithub -a="git@github.com:wexample/scripts.git" -rm

# Remove wexample.sh
rm -rf $w
