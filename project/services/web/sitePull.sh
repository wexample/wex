#!/usr/bin/env bash

webSitePull() {
  . .wex

  chown -R www-data:www-data ./project/
}