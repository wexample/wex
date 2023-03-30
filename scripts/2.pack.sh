#!/usr/bin/env bash

APP_NAME='wex'
VERSION='5.0.0~beta.3'
BUILD_NAME="${APP_NAME}_${VERSION}"
PATH_ROOT="$(realpath "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/"
PATH_BUILD="${PATH_ROOT}builds/"
PATH_BUILD_BUILD="${PATH_BUILD}${BUILD_NAME}/"
PATH_BUILD_SOURCE="${PATH_BUILD_BUILD}wex"
cd "${PATH_ROOT}" || return

sudo chown -R owner:owner "${PATH_BUILD}"

# Only "cli" folder is executable
cd "${PATH_BUILD_BUILD}" || return
sudo chmod -R -x wex
sudo chmod -R +x wex/cli
sudo find wex/ -name "*.sh" -type f -exec chmod +x {} \;

# All "folders" have 755 permission
sudo find . -type d -exec chmod 755 {} \;

# Build.
debuild -us -uc

## Sign
#cd /var/www/build/workdir/ || return
#debsign -k contact@wexample.com wex_5.0.0~beta.2-1_amd64.changes
