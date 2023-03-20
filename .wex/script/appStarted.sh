#!/usr/bin/env bash

_wexLog "Running custom app scripts"

CONTAINER_USER=owner

# Share current user identity
GIT_USER_NAME=$(git config --global user.name)
GIT_USER_EMAIL=$(git config --global user.email)
wex app::app/exec -vv -u=${CONTAINER_USER} -c="git config --global user.name '${GIT_USER_NAME}'"
wex app::app/exec -vv -u=${CONTAINER_USER} -c="git config --global user.email '${GIT_USER_EMAIL}'"

_wexLog "Copying .git inside container"
docker cp .git $(wex app/container -c=dev):/var/www/html

_wexLog "Copying ssh credentials inside container"
docker cp ~/.ssh/ $(wex app/container -c=dev):/home/${CONTAINER_USER}/

# Enforce asking passphrase for ssh key.
wex app::app/exec -vv -u="cd /var/www/html && git status"

# Install wex.
wex app::app/exec -vv -c=". /var/www/html/cli/install"

