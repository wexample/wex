#!/usr/bin/env bash

dockerIsEnv() {
  if [ -f /.dockerenv ]; then
      echo true
  else
      echo false;
  fi
}
