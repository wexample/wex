#!/usr/bin/env bash

rootLoginEnable() {
  # Change local config.
  wex config/changeValue -f=/etc/ssh/sshd_config -k=PermitRootLogin -v=yes
  # Reload
  service ssh restart
}
