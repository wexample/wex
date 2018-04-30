#!/usr/bin/env bash
# Source this file to execute install and add wexample to PATH

# Install wexample
w=_install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/project/bash/default/$w | tr -d '\015' > $w && . $w && rm -rf $w
