#!/usr/bin/env bash

# Install base configuration on a server managed by wexample.
vpsInit() {
  apt-get install git dos2unix zip -yqq
  # Install docker.
  wex docker/install
  # Disable root login
  wex rootLogin/disable
  # Create www dir
  mkdir -p /var/www/

  # TODO TEST IT
  #wex config/setValue /etc/ssh/sshd_config -k="Port" -v=""
  #service ssh restart
}
