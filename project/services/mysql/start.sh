#!/usr/bin/env bash

mysqlAppStart() {
  # Create dir, mod expected for mysql init.
  mkdir -p -m 777 ./mysql/data
  mkdir -p -m 777 ./mysql/dumps
}