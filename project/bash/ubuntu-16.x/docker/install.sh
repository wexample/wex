#!/usr/bin/env bash

dockerInstall() {
  # If no release candidate
  # Edit :  /etc/apt/sources.list
  # Add / Change : deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable
  # apt-get update
  # apt-get install docker-ce

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

  sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-propnano doc erties-common \
    -yqq

   apt-get install docker-ce docker-compose -yqq
}
