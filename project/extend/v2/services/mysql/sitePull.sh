#!/usr/bin/env bash

mysqlSitePull() {
  . .wex
  # Need
  docker exec ${SITE_NAME_INTERNAL}_mysql chown -R mysql:mysql /var/lib/mysql
}