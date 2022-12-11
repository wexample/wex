#!/usr/bin/env bash

systemArch() {
  if [ "$(uname -m)" = 'x86_64' ]; then
    echo 64
  else
    echo 32
  fi
}
