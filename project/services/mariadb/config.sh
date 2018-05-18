#!/usr/bin/env bash

mariadbConfig() {
  wex service/templates -s=mariadb -e=cnf.json

  wex db/config
}
