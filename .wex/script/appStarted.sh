#!/usr/bin/env bash

_wexLog "Running custom app scripts"

CONTAINER_USER=owner

# Share current user identity
GIT_USER_NAME=$(sudo -u "${SUDO_USER}" git config --global user.name)
GIT_USER_EMAIL=$(sudo -u "${SUDO_USER}" git config --global user.email)
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.name '${GIT_USER_NAME}'"
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.email '${GIT_USER_EMAIL}'"

# Get rid of old branches
wex app::app/exec -vv -c="touch /home/owner/.gitconfig"
wex app::app/exec -vv -c="chown -R ${CONTAINER_USER}:${CONTAINER_USER} /home/owner/"
wex app::app/exec -vv -c="chown -R ${CONTAINER_USER}:${CONTAINER_USER} /opt/wex"
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="cd /opt/wex && git prune"

# Install wex locally, faking an apt install.
wex app::app/exec -vv -u="${CONTAINER_USER}" -c=". /opt/wex/cli/install"
