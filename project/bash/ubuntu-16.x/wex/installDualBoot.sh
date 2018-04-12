#!/usr/bin/env bash

# Install feature to suppor wex on a dual boot linux / windows system
# It will stop docker containers when linux stops
# in order to avoid conflicts with shared drives.
wexInstallDualBoot() {
  # Start
  rm -f /etc/init.d/wexDualBootStart.sh
  # Copy start content at the beginning of rc.local
  echo -e "$(cat ${WEX_DIR_ROOT}samples/dualBoot/start.sh)\n\n$(cat /etc/rc.local)" > /etc/rc.local

  # Stop
  rm -f /etc/init.d/wexDualBootStop.sh
  rm -f /etc/rc0.d/K99wexDualBootStop
  rm -f /etc/rc6.d/K99wexDualBootStop
  # Copy main file
  cp ${WEX_DIR_ROOT}samples/dualBoot/stop.sh /etc/init.d/wexDualBootStop.sh
  # Symlink on Reboot
  ln -s /etc/init.d/wexDualBootStop.sh /etc/rc0.d/K99wexDualBootStop
  # Symlink on Shutdown
  ln -s /etc/init.d/wexDualBootStop.sh /etc/rc6.d/K99wexDualBootStop

}