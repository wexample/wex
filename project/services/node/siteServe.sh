#!/usr/bin/env bash

nodeSiteServe() {
  wex site/exec -c="service nginx restart"
}