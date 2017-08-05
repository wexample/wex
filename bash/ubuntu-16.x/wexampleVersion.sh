#!/usr/bin/env bash

wexampleVersion() {
  echo '1.'$(git rev-list --all --count --git-dir=${WEX_LOCAL_DIR}.git --work-tree=${WEX_LOCAL_DIR})
}
