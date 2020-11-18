#!/usr/bin/env bash

mysql8SitePull() {
  . .wex
  # Need
  docker exec ${SITE_NAME_INTERNAL}_mysql chown -R mysql:mysql /var/lib/mysql
}