#!/usr/bin/env bash

apacheRestart() {
  . ${WEX_APP_CONFIG}

  wex app/exec -su -c="service apache2 restart"
}
