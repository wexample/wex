#!/usr/bin/env bash

laravel5Update() {
    # Same as web
  . ${WEX_DIR_ROOT}services/symfony4/update.sh

  symfony4Update
}