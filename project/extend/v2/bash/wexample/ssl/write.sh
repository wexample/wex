#!/usr/bin/env bash

sslWrite() {
  local DOMAINS=$(wex app/domains)
  local CONFIG='';

  CONFIG+="  #SSLEngine on\n";
  CONFIG+="  #SSLCertificateFile /certs/${DOMAINS}.crt\n";
  CONFIG+="  #SSLCertificateKeyFile /certs/${DOMAINS}.key";

  echo -e "${CONFIG}" > ${WEX_WEXAMPLE_SITE_DIR_TMP}/web.ssl.conf
}