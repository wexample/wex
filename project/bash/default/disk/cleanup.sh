#!/usr/bin/env bash

diskCleanup() {
  # Remove all unused packages
  apt-get autoclean

  if [ $(wex package/exists -n=docker) == true ];then
      # Remove unused docker images.
      docker system prune --all
  fi

  if [ $(wex package/exists -n=docker) == true ];then
      # Remove unused docker images.
      docker system prune --all
  fi
}