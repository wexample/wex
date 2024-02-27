#!/bin/bash

# Testing usage
# This file is mounted inside the remote test container
# It will create a copy of and app (i.e. test-app-123456)
# from "test" env to "test_remote" env.
# The goal is to create a copy of a local app to a remote environments
# in order to test file synchronization between them.

APP_DIR_NAME=$1
APP_TEST_REMOTE_DIR="/var/www/test_remote/${APP_DIR_NAME}/"


echo "____________________"
echo "APP_DIR_NAME:${APP_DIR_NAME}"
echo "APP_TEST_REMOTE_DIR:${APP_TEST_REMOTE_DIR}"
realpath .
ls -la "/var/www/"
ls -la "/var/www/test/"
ls -la "/var/www/test/${APP_DIR_NAME}"
ls -la "/var/www/test/${APP_DIR_NAME}.wex"
ls -la "/var/www/test/${APP_DIR_NAME}.wex/cron"
echo "____________________"

echo "Remove old one ${APP_TEST_REMOTE_DIR}"
rm -rf "${APP_TEST_REMOTE_DIR}"

echo "Copy from local env ${APP_TEST_REMOTE_DIR}"
mkdir -p "${APP_TEST_REMOTE_DIR}"
cp -r "/var/www/test/${APP_DIR_NAME}" "${APP_TEST_REMOTE_DIR}"

# Start proxy manually to define test ports
wex app::helper/start -n proxy -p 3335 -ps 3336 -e test_remote

wex app::webhook/listen -a -p 12123

# Go to app dir
cd "${APP_TEST_REMOTE_DIR}"
touch "${APP_TEST_REMOTE_DIR}.wex/cron/test_remote"

echo "APP_DIR_NAME:${APP_DIR_NAME}"
echo "APP_TEST_REMOTE_DIR:${APP_TEST_REMOTE_DIR}"
realpath .

wex app::app/start -e test_remote
