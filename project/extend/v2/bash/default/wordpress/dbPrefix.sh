#!/usr/bin/env bash

wordpressDbPrefix() {
  grep -oP "\\\$table_prefix.+?'\K[^']+" ./wp-config.php
}