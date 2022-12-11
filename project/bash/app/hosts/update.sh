#!/usr/bin/env bash

hostsUpdate() {
  # Rebuild hosts file
  local IP=$(wex docker/ip)
  local REGISTRY=$(cat ${WEX_PROXY_APPS_REGISTRY})
  local HOSTS_FILE=""
  local DIR=""

  for DIR in ${REGISTRY[@]}
  do
    local DOMAINS=($(wex app/domains -d=${DIR}))
    local DOMAIN=""

    for DOMAIN in ${DOMAINS[@]}
    do
      # Prevent IP address to be sent as domain link in reverse proxy.
      if [ "${DOMAIN}" != "${IP}" ];then
        HOSTS_FILE+="\n"${IP}"\t"${DOMAIN}
      fi
    done;
  done;

  # Store hosts list.
  echo -e ${HOSTS_FILE} | sudo tee ${WEX_DIR_PROXY_TMP}hosts > /dev/null
}
