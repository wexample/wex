#!/usr/bin/env bash

webInit() {
  . .wex
  sed -i 's/domain.com/'${PROD_DOMAIN_MAIN}'/g' ./apache/web.prod.conf
}