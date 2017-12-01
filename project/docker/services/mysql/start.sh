#!/usr/bin/env bash

mysqlStart() {
  # Load default login / password if not specified.
  wex wexample::db/credentialsDefault
}
