#!/usr/bin/env bash

sshPasswordAuth() {
  # Disable password authentication
  configFile=/etc/ssh/ssh_config

  wexample configSetValue ${configFile} 'PasswordAuthentication' ${1}

  # May display an error when running from Docker
  # https://stackoverflow.com/questions/39169403/systemd-and-systemctl-within-ubuntu-docker-images
  systemctl reload sshd
}
