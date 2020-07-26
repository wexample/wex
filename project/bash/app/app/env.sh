#!/usr/bin/env bash

appEnv() {
  wex bash/readVar -f=${WEX_WEXAMPLE_APP_FILE_ENV} -k=SITE_ENV
}