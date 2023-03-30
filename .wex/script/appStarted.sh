#!/usr/bin/env bash

_wexLog "Running custom app scripts"

CONTAINER_USER=owner

# Share current user identity
GIT_USER_NAME=$(sudo -u "${SUDO_USER}" git config --global user.name)
GIT_USER_EMAIL=$(sudo -u "${SUDO_USER}" git config --global user.email)
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.name '${GIT_USER_NAME}'"
wex app::app/exec -vv -u="${CONTAINER_USER}" -c="git config --global user.email '${GIT_USER_EMAIL}'"

# Give root permission.
wex app::app/exec -vv -c="chown -R root:root /root/.gnupg"
wex app::app/exec -vv -c="chmod 700 /root/.gnupg"

# For debian package
wex app::app/exec -vv -c="export DEBEMAIL='${GIT_USER_EMAIL}'"

# Get rid of old branches

wex app::app/exec -vv -c="touch /home/owner/.gitconfig"
wex app::app/exec -vv -c="chown -R ${CONTAINER_USER}:${CONTAINER_USER} /home/owner/"
