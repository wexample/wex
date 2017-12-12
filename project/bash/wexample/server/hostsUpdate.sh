#!/usr/bin/env bash

serverHostsUpdate() {
  # Rebuild hosts file
  IP=$(wex docker/ip)
  REGISTRY=$(cat ${WEX_WEXAMPLE_DIR_PROXY_TMP}sites)
  HOSTS_FILE=""

  for DIR in ${REGISTRY[@]}
  do
    wex site/domains -d=${DIR}
    DOMAINS=($(wex site/domains -d=${DIR}))

    for DOMAIN in ${DOMAINS[@]}
    do
      HOSTS_FILE+="\n"${IP}"\t"${DOMAIN}
    done;
  done;

  # Store hosts list.
  echo -e ${HOSTS_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
