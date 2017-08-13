#!/usr/bin/env bash

# User to install a new non docker server.
#  user=${1}
#  password=${2}
#  group=sudo

user="wexample"
password="wex"
group=sudo

apt-get update -yqq

# New core user
wexample userAdd "${user}" "${password}" "${group}"

# SSH
key=$(< ${WEX_DIR_ROOT}ssh/id_rsa.pub)
wexample sshAddUser "${user}" "${group}" "'"${key}"'"

# Set custom port.
wexample sshSetPort 2299
wexample sshPasswordAuth 'no'

# Init firewall.
wexample firewallInitSetup

# Install docker.
wexample dockerInstall

# TODO May be into a container ?
# wexample letsEncryptInstall "wexample.com" "contact@wexample.com" "/var/www/wexample"
