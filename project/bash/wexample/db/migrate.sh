#!/usr/bin/env bash

dbMigrate() {
  wex hook/exec -c=dbMigrate
}