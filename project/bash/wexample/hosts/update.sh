#!/usr/bin/env bash

hostsUpdate() {
  # Rebuild hosts file
  local IP=$(wex docker/ip)
  local REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  local HOSTS_FILE=""
  local DIR=""

  for DIR in ${REGISTRY[@]}
  do
    local DOMAINS=($(wex site/domains -d=${DIR}))
    local DOMAIN=""

    for DOMAIN in ${DOMAINS[@]}
    do
      HOSTS_FILE+="\n"${IP}"\t"${DOMAIN}
    done;
  done;

  # Store hosts list.
  echo -e ${HOSTS_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
