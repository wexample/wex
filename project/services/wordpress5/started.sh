#!/usr/bin/env bash

wordpress5Started() {
  . .wex

  _wexLog "Wait mounted volumes to be available..."
  sleep 5

  wex site/serve
}