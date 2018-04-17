#!/usr/bin/env bash

serverDashboard() {
  wex web/open -u='http://'$(wex docker/ip)
}