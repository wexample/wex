#!/usr/bin/env bash

dockerCleanUp() {
  # Cleanup
  docker system prune -f
}
