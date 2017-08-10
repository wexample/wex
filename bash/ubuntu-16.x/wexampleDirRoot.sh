#!/usr/bin/env bash

wexampleDirRoot() {
  echo $(realpath $(wexample pathSafe ${WEX_DIR_ROOT}))"/";
}
