#!/usr/bin/env bash

sshSetPort() {
  # Set a custom port for SSH
  wexample configChangeValue /etc/ssh/sshd_config Port ${1}
  service ssh restart
}
