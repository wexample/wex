#!/usr/bin/env bash

cd ${WEX_DIR_ROOT}../

wex git/resetHard
# TODO
wex wexample::images/rebuild -d -u=${DOCKER_HUB_USERNAME} -p=${DOCKER_HUB_PASSWORD}

wex wex/grantRights
