#!/usr/bin/env bash

wexampleDirRoot() {
  echo $(realpath $(wex path/safe -p=${WEX_DIR_ROOT}))"/";
}
