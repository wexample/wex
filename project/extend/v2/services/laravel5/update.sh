#!/usr/bin/env bash

laravel5Update() {
    # Same as web
  . ${WEX_DIR_SERVICES}symfony4/update.sh

  symfony4Update
}