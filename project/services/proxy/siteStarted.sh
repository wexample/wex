#!/usr/bin/env bash

proxySiteStarted() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Copy FTP access to FTP global container.
  local FTP_PASSWD=./ftp/passwd/${SITE_NAME}.passwd
  # Access file exists.
  if [ -f ${FTP_PASSWD} ];then
    docker cp ${FTP_PASSWD} wex_ftp:/etc/pure-ftpd/passwd/${SITE_NAME}.passwd
    # Reload FTP service.
    docker exec wex_ftp service pure-ftpd force-reload
  fi
}