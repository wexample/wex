#!/usr/bin/env bash

_wexLog "Running custom app scripts"

# Share current user identity
GIT_USER_NAME=$(git config --global user.name)
GIT_USER_EMAIL=$(git config --global user.email)
wex app::app/exec -vv -c="git config --global user.name ${GIT_USER_NAME}"
wex app::app/exec -vv -c="git config --global user.email ${GIT_USER_EMAIL}"

_wexLog "Copying .git inside container"
docker cp .git $(wex app/container -c=dev):/var/www/html

# Install wex.
wex app::app/exec -vv -c=". /var/www/html/cli/install"

