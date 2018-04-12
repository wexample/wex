#!/usr/bin/env bash

cronReload() {
  wex site/exec -c="crontab /var/default.cron"
}
