#!/usr/bin/env bash

wexampleVersion() {
  echo '1.'$(${WEX_DIR_ROOT} git rev-list --all --count)
}
