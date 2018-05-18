#!/usr/bin/env bash

odooConfig() {
  wex db/config

  echo "\nSITE_CONTAINER=odoo"
}
