#!/usr/bin/env bash

ftpUserAddArgs() {
  _ARGUMENTS=(
    [0]='ftp_username u "FTP Username" true'
    [1]='password p "Password" true'
    [2]='directory d "Directory related to site root (ex : project/files)" true'
  )
}

ftpUserAdd() {
  # Load site name.
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Exec into container
  #docker exec -ti wex_ftp
  echo "echo ${PASSWORD}; echo ${PASSWORD} | pure-pw useradd ${FTP_USERNAME} -f /etc/pure-ftpd/passwd/${SITE_NAME}.passwd -m -u ftpuser -d /var/www/${SITE_NAME}/${DIRECTORY}"

  #wex ftp/save
}
