#!/usr/bin/env bash

# This file is called by SSH to execute script with wexample context.
# Wexample is loaded from .bashrc by default which is not loaded
# during deployment from SSH.

# The better approach may be to create a real bundle with wexample scripts,
# or install it into profile.

# Install wexample.
#. /opt/wexample/project/bash/ubuntu-16.x/_installLocal.sh

#ls -la

#echo "Execute : "${1}

# Run script.
#${1}

echo "__________"
