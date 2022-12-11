#!/usr/bin/env bash

dockerInstallArgs() {
  _AS_SUDO=true
  _DESCRIPTION="Install Docker on current machine"
}

dockerInstall() {
  # If no release candidate
  # Edit :  /etc/apt/sources.list
  # Add / Change : deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable
  # apt-get update
  # apt-get install docker-ce

  # Do not install docker on docker.
  if [ $(wex docker/isEnv) == true ];then
    return
  fi

  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

  apt-get update

  # TODO Last changes not tested.
  apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    doc \
    docker-ce \
    docker-compose \
    erties-common \
    software-propnano \
    -yq
}
