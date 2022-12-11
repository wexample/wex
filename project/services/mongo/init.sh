#!/usr/bin/env bash

mongoInit() {
  wex site/start -c=mongo

  # Override default container.
  echo "MONGO_VERSION=5.0.3-focal" >> .wex

  echo "Wait 20 seconds for database fill.."

  wex site/stop
}
