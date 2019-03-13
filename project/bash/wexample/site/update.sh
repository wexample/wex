#!/usr/bin/env bash

siteUpdate() {
  # Call services hooks.
  wex hook/exec -c=update
}