#!/usr/bin/env bash

# See wex wexample::vps/remoteInit for a usage of this script.

# Get last production version.
curl -Lo /opt/wexample.zip https://github.com/wexample/scripts/archive/master.zip
# Extract
unzip /opt/wexample.zip -d /opt/
# Move
mv /opt/scripts-master/ /tmp/wexample
# Install locally.
bash /opt/wexample/project/bash/default/_installLocal.sh