#!/usr/bin/env bash

siteEnvArgs() {
  _MIGRATED_TO_V3=true
}

siteEnv() {
  ${WEX_DIR_V3_CMD} bash/readVar -f=.env -k=SITE_ENV
}