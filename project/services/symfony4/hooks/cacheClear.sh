#!/usr/bin/env bash

symfony4CacheClear() {
  wex app/exec -l -c="php bin/console cache:clear"
}