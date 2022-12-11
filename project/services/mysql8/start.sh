#!/usr/bin/env bash

mysql8Start() {
  # Create dir, mod expected for mysql init.
  mkdir -p -m 777 ./mysql/data
  mkdir -p -m 777 ./mysql/dumps
}