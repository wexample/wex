#!/usr/bin/env bash

firewallInitSetup() {
  # Firewall
  # Install if not exists
  apt-get install ufw -yqq

  # TODO Docker only : Disallow IPV6 to prevent firewall warnings
  # wexample configSetValue /etc/default/ufw "IPV6" "no" "="

  # Allow SSH
  ufw allow OpenSSH
  ufw --force enable
}
