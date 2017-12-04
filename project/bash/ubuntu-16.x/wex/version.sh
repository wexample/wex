#!/usr/bin/env bash

wexVersion() {
  cd ${WEX_LOCAL_DIR}
  echo '1.'$(git rev-list --all --count)
}
