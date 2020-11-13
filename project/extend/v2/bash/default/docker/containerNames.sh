#!/usr/bin/env bash

dockerContainerNames() {
  NAMES=($(docker ps --format '{{.Names}}'))
  echo ${NAMES[@]}
}
