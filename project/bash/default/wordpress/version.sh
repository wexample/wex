#!/usr/bin/env bash

wordpressVersionArgs() {
  _ARGUMENTS=(
    'file f "Settings file path" false "./wp-includes/version.php"'
  )
}

wordpressVersion() {
  grep -oP "\\\$wp_version.+?'\K[^']+" "${FILE}"
}