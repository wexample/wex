#!/usr/bin/env bash

wordpressVersion() {
  # Use base command inside container.
  wex app/exec -l -c="wex wordpress/version"
}