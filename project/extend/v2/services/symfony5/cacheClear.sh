#!/usr/bin/env bash

symfony5CacheClear() {
  wex site/exec -l -c="php bin/console cache:clear"
}