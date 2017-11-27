#!/usr/bin/env bash

serverRestart() {
  wex server/stop
  wex server/start
}
