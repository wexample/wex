#!/usr/bin/env bash

webSslEnable() {
  local ENV=${1}
  # Enable apache SSL
  wex config/uncomment -k=ServerName -s=" " -f=./apache/web.${ENV}.conf
  wex config/uncomment -k=SSLEngine -s=" " -f=./apache/web.${ENV}.conf
  wex config/uncomment -k=SSLCertificateFile -s=" " -f=./apache/web.${ENV}.conf
  wex config/uncomment -k=SSLCertificateKeyFile -s=" " -f=./apache/web.${ENV}.conf
}