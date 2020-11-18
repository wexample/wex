#!/usr/bin/env bash

rootLoginDisable() {
  # Change local config.
  wex config/changeValue -f=/etc/ssh/sshd_config -k=PermitRootLogin -v=no
  # Reload
  service ssh restart
}
