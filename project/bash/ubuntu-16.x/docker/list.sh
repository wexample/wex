#!/usr/bin/env bash

dockerList() {
  docker ps --format "{{.Names}}\t{{.Status}}\t{{.Ports}}"
}