#!/bin/bash
#
## Remove built in scripts
#rm -rf /opt/wexample
## Copy current (let a copy in place for ci tools)
#cp -r /builds/wexample-public/scripts /opt/wexample
## Go to
#cd /opt/wexample
#
## Load wexample.
#bash ./bash/ubuntu-16.x/_installLocal.sh
#
## Init gitlab
#wex gitlab/init
#
## Install composer : we use some libraries in PHP scripts
#wex composer/pharInstall
#
## Run all tests
##bash bash/ubuntu-16.x/_tests/_run.sh
#
#cd /builds/wexample-public/scripts

# Add SSH key.
apt-get install openssh-client -yqq
mkdir -p ~/.ssh
eval $(ssh-agent -s)
[[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

# Add ssh user.
ssh-add <(echo "$STAGING_PRIVATE_KEY")

# Deploy to GitHub
wex gitlab/deployGithub -r="git@github.com:wexample/scripts.git" -k=${STAGING_PRIVATE_KEY}
