#!/usr/bin/env bash

dockerList() {
  docker ps -a --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
}