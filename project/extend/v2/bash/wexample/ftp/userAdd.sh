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
  . ${WEX_APP_CONFIG}
  . .wex

  # TODO Does not work : use default generate file instead (no -f)
  local PASS_LOCATION=/etc/pure-ftpd/passwd/wex.passwd

  docker exec -ti wex_ftp touch ${PASS_LOCATION}
  # Exec into container
  docker exec -ti wex_ftp /bin/bash -c "(echo ${PASSWORD}; echo ${PASSWORD}) |  pure-pw useradd ${SITE_NAME_INTERNAL}_${FTP_USERNAME} -f ${PASS_LOCATION} -m -u ftpuser -d /var/www/${SITE_ENV}/${SITE_NAME}/${DIRECTORY}"
}
