#!/usr/bin/env bash

serverStart() {
  docker-compose -f ${WEX_DIR_ROOT}samples/docker/docker-compose.proxy.yml up -d
}
