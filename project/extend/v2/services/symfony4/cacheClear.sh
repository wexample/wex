#!/usr/bin/env bash

symfony4CacheClear() {
  wex site/exec -l -c="php bin/console cache:clear"
}