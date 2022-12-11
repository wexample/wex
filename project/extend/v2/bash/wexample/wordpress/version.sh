#!/usr/bin/env bash

wordpressVersion() {
  # Use base command inside container.
  wex site/exec -l -c="wex wordpress/version"
}