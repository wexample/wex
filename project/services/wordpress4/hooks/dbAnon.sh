#!/usr/bin/env bash

wordpress4DbAnon() {
  local IDS=$(wex app/exec -l -c="wp user list --allow-root --field=id")
  for ID in ${IDS[@]}
  do
    # Set all IDs to password.
    wex app/exec -l -c="wp user update $(wex string/trim -s="${ID}") --user_pass=password --allow-root --skip-email"
  done;
}