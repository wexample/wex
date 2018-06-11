#!/usr/bin/env bash

# See wex wexample::vps/remoteInit for a usage of this script.

# Get last production version.
# TODO We cant use properly scripts like that : it expect to have a .git repository to find de wex version number
curl -Lo /opt/wexample.zip https://github.com/wexample/scripts/archive/master.zip
# Extract
unzip /opt/wexample.zip -d /opt/
# Move
mv /opt/scripts-master/ /opt/wexample
# Install locally.
bash /opt/wexample/project/bash/default/_installLocal.sh