#!/usr/bin/env bash

gitlabSshInitArgs() {
  _ARGUMENTS=(
    [0]='private_key_file k "Private file key stored into project variables" true'
  )
}

gitlabSshInit() {
  # Add SSH and prevent host checking.
  apt-get install openssh-client -yqq

  mkdir -p ~/.ssh
  eval $(ssh-agent -s)
  [[ -f /.dockerenv ]] && echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config

  # Add ssh user.
  ssh-add <(cat ${PRIVATE_KEY_FILE})
}
