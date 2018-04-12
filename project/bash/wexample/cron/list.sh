#!/usr/bin/env bash

cronList() {
  wex site/exec -c="crontab -l"
}
