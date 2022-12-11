#!/usr/bin/env bash

wordpressVersion() {
  grep -oP "\\\$wp_version.+?'\K[^']+" ./wp-includes/version.php
}