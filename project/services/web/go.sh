#!/usr/bin/env bash

webGo() {
  # Do not execute action bu return it to be piped.
  echo "[ -d /var/www/html/project ] && cd /var/www/html/project || cd /"
}