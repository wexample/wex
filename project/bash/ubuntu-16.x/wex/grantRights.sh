#!/usr/bin/env bash

wexGrantRights() {
  cd ${WEX_DIR_ROOT}../
  # Git all needed wrights.
  chown root:root -R *
  chmod -R 755 *
}
