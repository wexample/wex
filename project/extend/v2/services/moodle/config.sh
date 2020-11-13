#!/usr/bin/env bash

moodleConfig() {
  . ${WEX_DIR_ROOT}services/web/config.sh
  webConfig

  # Override default container.
  echo "\nSITE_CONTAINER=moodle"
}