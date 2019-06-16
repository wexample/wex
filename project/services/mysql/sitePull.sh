#!/usr/bin/env bash

mysqlSitePull() {
  . .wex
  # Need
  docker exec ${NAME}_mysql chown -R mysql:mysql /var/lib/mysql
}