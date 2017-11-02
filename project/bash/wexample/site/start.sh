#!/usr/bin/env bash

siteStart() {
  wex site/compose -c="up -d --build"
}
