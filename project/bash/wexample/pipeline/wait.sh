#!/usr/bin/env bash

pipelineWait() {
  echo ''
  local MESSAGE="Waiting auto deployment..."
  while [ $(wex pipeline/ready) == false ];do
    echo -ne ${MESSAGE}"\r"
    MESSAGE+='.'
    sleep 2
  done
  echo ''
}