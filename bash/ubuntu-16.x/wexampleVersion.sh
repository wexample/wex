#!/usr/bin/env bash

wexampleVersion() {
  echo '1.'$(git rev-list --all --count)
}
