#!/bin/bash

echo "Installing local project to test remote"
source /opt/wex/.wex/python/venv/bin/activate
bash /opt/wex/cli/install

. /opt/wex/.wex/docker/test_remote/test_remote-entrypoint.sh