#!/usr/bin/env bash

wordpressStart() {
  # Give write access.
  chown -R www-data:www-data ./wordpress/
}