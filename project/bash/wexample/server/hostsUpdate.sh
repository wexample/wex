#!/usr/bin/env bash

serverHostsUpdate() {
  # Rebuild hosts file
  IP=$([[ $(command -v docker-machine) ]] && echo $(docker-machine ip) || echo localhost)
  SITES=$(wex server/sites)
  HOSTS_FILE=""

  for SITE in ${SITES[@]}
  do
    DIR=$(sed -n "s/^\(.*\)\=\(.*\)\$/\2/p" <<< ${SITE})
    DOMAINS=($(wex site/domains -d=${DIR}))

    for DOMAIN in ${DOMAINS[@]}
    do
      HOSTS_FILE+="\n"${IP}"\t"${DOMAIN}
    done;
  done;

  # Store hosts list.
  echo -e ${HOSTS_FILE} > ${WEX_WEXAMPLE_DIR_PROXY_TMP}hosts
}
