#!/usr/bin/env bash

ftpUserAddArgs() {
  _ARGUMENTS=(
    [0]='ftp_username u "FTP Username" true'
    [1]='directory d "Directory related to site root, ex : project/files " true'
  )
}

ftpUserAdd() {
  # Load site name.
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  # Check ftp container exists
  if [ $(wex docker/containerExists -c=${SITE_NAME}_ftp) == false ];then
    return
  fi

  # Exec into container
  docker exec -ti ${SITE_NAME}_ftp /bin/bash -c "pure-pw useradd ${FTP_USERNAME} -f /etc/pure-ftpd/passwd/pureftpd.passwd -m -u ftpuser -d /var/www/html/${DIRECTORY}"
}
