#!/usr/bin/env bash

ftpSaveArgs() {
  _ARGUMENTS=(
    [0]='tag t "Commit suffix" false'
  )
}

ftpSave() {
  # Load site name.
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Create dest dir.
  mkdir -p ./ftp/passwd
  # Copy file content.
  echo -e $(docker exec wex_ftp cat /etc/pure-ftpd/passwd/${SITE_NAME}.passwd) > ./ftp/passwd/${SITE_NAME}.passwd

  # Save.
  git add ./ftp/passwd
  git commit -m "ftp/userAdd ${TAG}"
  git push
}