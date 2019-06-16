#!/usr/bin/env bash

# TODO This is a tomporary file which is not used automatically
# This event should fire when pulling new data from repository

wex site/exec -l -c="yarn install --production=true"
wex site/exec -l -c="composer install"

wex site/perms
