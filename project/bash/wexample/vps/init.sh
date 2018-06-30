#!/usr/bin/env bash

vpsInitArgs() {
  _ARGUMENTS=(
    [0]='user u "Admin username that replace root" true'
    [1]='port p "New SSH port" true'
    [2]='password pw "New password" true'
    [3]='public_key pub "Public SSH key file to import as authorized keys" true'
  )
}

# Install base configuration on a server managed by wexample.
vpsInit() {

  # Create user
  wex user/create -u="${USER}" -p="${PASSWORD}" -g=sudo
  # Give sudo access.
  usermod -aG sudo ${USER}
  local USER_SSH_DIR=/home/${USER}/.ssh
  # Copy public
  if [ "${PUBLIC_KEY}" != "" ];then
    # Add given public key
    mkdir -p ${USER_SSH_DIR}
    cat ${PUBLIC_KEY} >> ${USER_SSH_DIR}/authorized_keys
    # Should be removed manually outside this script
  fi
  # Set right access
  chmod 600 ${USER_SSH_DIR}
  # Set login port Port
  wex config/setValue -f=/etc/ssh/sshd_config -k="Port" -v="${PORT}"
  # Disable root login
  wex rootLogin/disable
  # Save config for next login.
  service ssh restart
  # Confirm
  echo "Your new login information are : ${USER}@"$(wex system/ip)":"${PORT}

  # TODO Disable password login ? (only ssh)
  # TODO Create gitlab user for automated deployments.
  # - Add Gitlab in "visudo", is /etc/sudoers file : gitlab ALL=(ALL) NOPASSWD: ALL
  # - Add Gitlab SSH public key to authorized_keys (how to retrieve it ?)
  # - chmod 700 ~/.ssh
  # - chmod 600 ~/.ssh/authorized_keys
  # - chown -R gitlab:sudo /home/gitlab/.ssh
  # - Set : PasswordAuthentication no => /etc/ssh/sshd_config
  # - service ssh restart

  # PHP is used for sites frameworks detection,
  # we may suppress it in the future.
  apt-get install git dos2unix zip php -yqq
  # Install docker.
  wex docker/install
  # Create www dir
  mkdir -p /var/www/

}
