#!/usr/bin/env bash

siteEnv() {
  ${WEX_DIR_V3_CMD} bash/readVar -f=.env -k=SITE_ENV
}