#!/bin/bash

echo "Installing local project to test remote"
bash /opt/wex/cli/install

. /opt/wex/.wex/docker/test_remote-entrypoint.sh