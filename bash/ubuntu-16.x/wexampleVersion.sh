#!/usr/bin/env bash

wexampleVersion() {
  echo '1.'$(git rev-list --all --count --git-dir=${WEX_DIR_ROOT}.git --work-tree=${WEX_DIR_ROOT})
}
