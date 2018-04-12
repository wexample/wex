#!/usr/bin/env bash

siteRestart() {
  wex site/stop
  wex site/start
}
