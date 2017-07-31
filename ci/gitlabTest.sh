#!/bin/bash

# We need to install dependencies only for Docker
[[ ! -e /.dockerenv ]] && exit 0

set -xe

# Install global packages
apt-get update -yqq

# Wexample loader for multiple scripts.
w=wexample.sh
curl https://raw.githubusercontent.com/wexample/scripts/master/bash/ubuntu-16.x/$w | tr -d '\015' > $w

# Remove warning on new SSH host.
bash $w -s=gitlabInstallComposer -rm
