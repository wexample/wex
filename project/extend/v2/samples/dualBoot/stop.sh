#!/usr/bin/env bash

# See wex wex/installDualBoot

# Stop all docker activity.
# If docker container are still running, it prevent
# to mount OS shared drive, and it move it on OS1 on next restart.
# By cleaning up all docker containers and networks we allow
# OS drive to be mounted on the same place on next boot.
wex docker/stopAll