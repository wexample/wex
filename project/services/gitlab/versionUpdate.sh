#!/usr/bin/env bash

# TODO This script is not used, we may automate migration in the future.

# To update Gitlab, just change the version of your actively running instance in the .wex file.
# This script should :

# Get the last version of gitlab docker image (remotely ?)
# Compare if there is an update
# Make a backup
# Stop the container
# Update the .wex file
# Start the container
# Allow a method to save any kind of errors, ex : gitlab expect to migrate from the last stable version
#   ex : 11.10.0 > 11.11.5 to migrate to the version 12
#   in this case we need to chain all upgrade processes.