#!/usr/bin/env bash

apacheRestart() {
  . ${WEX_WEXAMPLE_SITE_CONFIG}

  docker exec $(wex site/container -c="") service apache2 restart
}
