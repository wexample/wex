#!/usr/bin/env bash

mongoInit() {
  wex site/start -c=mongo

  echo "Wait 20 seconds for database fill.."

  wex site/stop
}
