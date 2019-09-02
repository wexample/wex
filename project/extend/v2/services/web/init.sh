#!/usr/bin/env bash

webInit() {
  . .wex
  sed -i"${WEX_SED_I_ORIG_EXT}" 's/domain.com/'${PROD_DOMAIN_MAIN}'/g' ./apache/web.prod.conf
  echo "WP_CORE_VERSION=4.9.5" >> .wex
}