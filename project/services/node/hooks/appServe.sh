#!/usr/bin/env bash

nodeAppServe() {
  wex app/exec -c="service nginx restart"
}