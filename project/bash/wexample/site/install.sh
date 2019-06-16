#!/usr/bin/env bash

siteInstall() {
  # Call services hooks.
  wex hook/exec -c=install
}