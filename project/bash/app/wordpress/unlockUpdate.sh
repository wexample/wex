#!/usr/bin/env bash

wordpressUnlockUpdateArgs() {
  _DESCRIPTION="Fix ‘Another Update in Process’ Error"
}

wordpressUnlockUpdate() {
  wex db/exec -c="DELETE FROM $(wex wordpress/dbPrefix)options WHERE option_name = 'core_updater.lock'"
}