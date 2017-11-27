#!/usr/bin/env bash

wexDirRoot() {
  echo $(realpath $(wex path/safe -p=${WEX_DIR_ROOT}))"/";
}
