#!/usr/bin/env bash

wordpressDbPrefixArgs() {
  _DESCRIPTION="Find database tables prefix"
}

wordpressDbPrefix() {
  . .wex

  if [ "${WP_DB_TABLE_PREFIX}" ];then
    echo ${WP_DB_TABLE_PREFIX}
  fi;

  echo 'wp_'
}