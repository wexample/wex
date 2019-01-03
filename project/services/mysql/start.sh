#!/usr/bin/env bash

mysqlStart() {
  # Create dir, mod expected for mysql init.
  mkdir -p -m 777 ./mysql/data
  mkdir -p -m 777 ./mysql/dumps
}