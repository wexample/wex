#!/usr/bin/env bash

wexampleDirRoot() {
  echo $(realpath $(wex path/safe ${WEX_DIR_ROOT}))"/";
}
