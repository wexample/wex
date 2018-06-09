#!/usr/bin/env bash

# Executing this file :
# w=install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/project/$w | tr -d '\015' > $w && . $w && rm $w

# Get last production version.
curl -Lo /opt/wexample.zip https://github.com/wexample/scripts/archive/master.zip
# Extract
unzip /opt/wexample.zip -d /opt/
# Move
mv /opt/scripts-master/ /tmp/wexample
# Install locally.
bash /opt/wexample/project/bash/default/_installLocal.sh