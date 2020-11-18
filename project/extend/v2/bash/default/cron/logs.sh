#!/usr/bin/env bash

cronLogs() {
  grep CRON /var/log/syslog
}
