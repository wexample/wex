#!/bin/bash

# Testing usage
# This file is mounted inside the remote test container
# It will create a copy of and app (i.e. test-app-123456)
# from "test" env to "test_remote" env.
# The goal is to create a copy of a local app to a remote environments
# in order to test file synchronization between them.

APP_DIR_NAME=$1
APP_TEST_REMOTE_DIR="/var/www/test_remote/${APP_DIR_NAME}/"

echo "Remove old one ${APP_TEST_REMOTE_DIR}"
rm -rf "${APP_TEST_REMOTE_DIR}"

echo "Copy from local env ${APP_TEST_REMOTE_DIR}"
cp -r "/var/www/test/${APP_DIR_NAME}" "${APP_TEST_REMOTE_DIR}"

# Go to app dir
cd "${APP_TEST_REMOTE_DIR}"
touch "${APP_TEST_REMOTE_DIR}.wex/cron/test_remote"

# Start proxy manually to define test ports
wex app::helper/start -n proxy -p 3335 -ps 3336 -e test_remote

wex app::webhook/listen -a -p 12123

wex app::app/start -e test_remote
