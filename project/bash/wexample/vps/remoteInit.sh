#!/usr/bin/env bash

vpsRemoteInitArgs() {
 _ARGUMENTS=(
   [0]='host h "Server host address" true'
   [1]='user u "Root username for first access" true'
   [2]='password pw "SSH Password" false'
   [3]='port p "SSH Port" false'
   [4]='new_user nu "New user for future root access" true'
   [5]='new_password npw "New password for user" true'
   [6]='new_port np "New port for future root access" true'
 )
}

vpsRemoteInit() {
  if [ "${PORT}" == "" ];then
    PORT=22
  fi

  # Display available beys
  wex ssh/keySelectList -pub
  local SSH_PUBLIC_KEY=$(wex ssh/keySelect -pub -d="SSH Public key for server")
  local PUBLIC_KEY_NAME=$(basename ${SSH_PUBLIC_KEY})

  # Transfer public key file
  scp -r -P${PORT} ${SSH_PUBLIC_KEY} ${USER}@${HOST}:"~/"

  local COMMAND=""
  # Install minimal packages.
  COMMAND+="apt-get update && apt-get install unzip -yqq "
  # Install wex scripts.
  COMMAND+="&& w=install.sh && curl https://raw.githubusercontent.com/wexample/scripts/master/\$w | tr -d '\\015' > \$w && . \$w && rm \$w "
  # Execute the rest of scripts
  COMMAND+="&& wex wexample::vps/init -u=\"${NEW_USER}\" -p=${NEW_PORT} -pub=~/${PUBLIC_KEY_NAME} "
  # Remove temp public key.
  COMMAND+="&& rm ${REMOTE_PUBLIC_KEY} "

  # Execute in one line to avoid more password asking.
  ssh -q ${USER}@${HOST} "${COMMAND}"
}