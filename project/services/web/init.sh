#!/usr/bin/env bash

webAppInit() {
  . .wex
  sed -i"${WEX_SED_I_ORIG_EXT}" 's/domain.com/'${PROD_DOMAIN_MAIN}'/g' ./apache/web.prod.conf
  rm ./apache/web.prod.conf${WEX_SED_I_ORIG_EXT}
}