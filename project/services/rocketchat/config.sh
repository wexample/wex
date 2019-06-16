#!/usr/bin/env bash

rocketchatConfig() {
  echo "\nSITE_CONTAINER=rocketchat"

  . .wex

  echo "\nROCKETCHAT_VERSION=${ROCKETCHAT_VERSION}"
}
