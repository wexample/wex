#!/usr/bin/env bash

siteIsset() {
  if [ -f ".wex" ];then
    echo true
  else
    echo false
  fi
}
