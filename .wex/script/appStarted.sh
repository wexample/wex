#!/usr/bin/env bash

_wexLog "Running custom app scripts"

CONTAINER_USER=owner

# Share current user identity
GIT_USER_NAME=$(git config --global user.name)
GIT_USER_EMAIL=$(git config --global user.email)
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.name '${GIT_USER_NAME}'"
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.email '${GIT_USER_EMAIL}'"

# Get rid of old branches

wex app::app/exec -vv -u="${CONTAINER_USER}" -c="cd /var/www/html && git prune"wex app::app/exec -vv -c="chown -R ${CONTAINER_USER}:${CONTAINER_USER} /var/www/html"
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="cd /var/www/html && git prune"

# Install wex.
wex app::app/exec -vv -u="${CONTAINER_USER}" -c=". /var/www/html/cli/install"

