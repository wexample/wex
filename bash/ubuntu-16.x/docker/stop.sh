#!/usr/bin/env bash

dockerStop() {
  # Stop composed containers
  docker-compose down
  # Stop all
  docker stop $(docker ps -qa)
  # Remove
  docker rm $(docker ps -qa)
}
