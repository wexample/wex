#!/usr/bin/env bash

coreUninstall() {
  rm /usr/local/bin/wex
  rm -rf ${WEX_DIR_INSTALL}
}
