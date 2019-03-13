#!/usr/bin/env bash

# Make current database anonymous (dev usage)
dbAnon() {
  wex hook/exec -c=dbAnon
}