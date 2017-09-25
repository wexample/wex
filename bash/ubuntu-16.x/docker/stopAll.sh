#!/usr/bin/env bash

dockerStopAll() {
  # Stop all
  docker stop $(docker ps -qa) -f
  # Remove
  docker rm $(docker ps -qa) -f
}
