#!/usr/bin/env bash

# Remove asking user to validate host keys on first SSH connexion.
sshRemoveHostChecking() {
  mkdir -p ~/.ssh
  eval $(ssh-agent -s)
  [[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
}
