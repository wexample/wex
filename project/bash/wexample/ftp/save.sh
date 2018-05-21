#!/usr/bin/env bash

ftpSave() {
  # Load site name.
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  docker exec -ti wex_ftp "cp /etc/pure-ftpd/passwd/${SITE_NAME}.passwd /var/www/${SITE_NAME}/ftp/passwd/"

  # Save.
  git add ./ftp/passwd/
  git commit -m "ftp/userAdd"
  git push
}