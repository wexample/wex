#!/usr/bin/env bash

siteIsset() {
  if [ -f "wex.json" ];then
    echo true
  else
    echo false
  fi
}
