#!/usr/bin/env bash

mysql8SitePull() {
  . .wex
  # Need
  docker exec ${SITE_NAME_INTERNAL}_${DB_CONTAINER} chown -R mysql:mysql /var/lib/mysql
}