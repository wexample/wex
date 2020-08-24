#!/usr/bin/env bash

proxyAppStarted() {
  . ${WEX_APP_CONFIG}

  # Copy FTP access to FTP global container.
  local FTP_PASSWD_LOCAL=./ftp/passwd/${SITE_NAME}.passwd
  # Access file exists.
  if [ -f ${FTP_PASSWD_LOCAL} ];then
    # File in ftp container.
    local FTP_PASSWD=/etc/pure-ftpd/passwd/${SITE_NAME}.passwd
    # Copy.
    docker cp ${FTP_PASSWD_LOCAL} wex_ftp:${FTP_PASSWD}
    # Give access.
    docker exec wex_ftp chmod 600 ${FTP_PASSWD}
    # Reload FTP service.
    docker exec wex_ftp service pure-ftpd force-reload
  fi
}