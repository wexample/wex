#!/usr/bin/env bash

wordpress5DbAnon() {
  local IDS=$(wex site/exec -l -c="wp user list --allow-root --field=id")
  for ID in ${IDS[@]}
  do
    # Set all IDs to password.
    wex site/exec -l -c="wp user update "$(${WEX_DIR_V3_CMD} string/trim -s=${ID})" --user_pass=password --allow-root --skip-email"
  done;
}