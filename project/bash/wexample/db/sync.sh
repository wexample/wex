#!/usr/bin/env bash

dbSync() {
  # TODO Test / Finish
  # Dump with pull
  wex db/dump -e=${ENVIRONMENT} -p
  #
  wex db/restore -d=${FILENAME???}
}
