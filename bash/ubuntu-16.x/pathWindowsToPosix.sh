#!/usr/bin/env bash

pathWindowsToPosix() {
  echo "/${1}" | sed -e 's/\\/\//g' -e 's/://'
}
