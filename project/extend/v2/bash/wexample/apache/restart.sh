#!/usr/bin/env bash

apacheRestart() {
  . ${WEX_APP_CONFIG}

  docker exec -u 0 $(wex site/container -c="") service apache2 restart
}
