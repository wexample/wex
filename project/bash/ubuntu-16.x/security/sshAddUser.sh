#!/usr/bin/env bash

sshAddUser() {
  user="${1}"
  group="${2}"
  key="${3}"

  # Create SSH dir.
  mkdir -p /home/${user}/.ssh

  chown ${user}:${group} /home/${user}/.ssh
  chmod 700 /home/${user}/.ssh

  # Add wexample SSH key
  wexample fileTextAppend /home/${user}/.ssh/authorized_keys "${key}"
  chown ${user}:${group} /home/${user}/.ssh/authorized_keys
  chmod 600 /home/${user}/.ssh/authorized_keys
}
