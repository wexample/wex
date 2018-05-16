#!/usr/bin/env bash

webInitEnv() {
  local ENV=${1}

  if [ ${ENV} != local ];then

    if [ ${ENV} != prod ];then
      cp ./apache/web.prod.conf ./apache/web.${ENV}.conf
    fi

    . .wex

    sed -i 's/domain.com/'${PROD_DOMAIN_MAIN}'/g' ./apache/web.${ENV}.conf

    wex config/uncomment -k=ServerName -s=" " -f=./apache/web.${ENV}.conf
    wex config/uncomment -k=SSLEngine -s=" " -f=./apache/web.${ENV}.conf
    wex config/uncomment -k=SSLCertificateFile -s=" " -f=./apache/web.${ENV}.conf
    wex config/uncomment -k=SSLCertificateKeyFile -s=" " -f=./apache/web.${ENV}.conf
  fi

}