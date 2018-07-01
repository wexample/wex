#!/usr/bin/env bash

siteInstall() {
  if [ $(wex site/isset) ];then
    # Add proper rights.
    chown www-data:www-data ./*
    # Call services hooks.
    wex service/exec -c=install
    # Call local ci hooks.
    wex ci/exec -c=install
  fi
}