#!/usr/bin/env bash

wexampleVersion() {
  cd ${WEX_LOCAL_DIR}
  echo '1.'$(git rev-list --all --count)
}
