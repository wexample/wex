#!/usr/bin/env bash

dbRollback() {
  # Load env name.
  wex site/loadEnv
  # Can't load this data into container.
  SITE_NAME=$(wex site/config -k=name)
  # Guess latest dump name.
  LATEST_DUMP_FILE=${SITE_ENV}"-"${SITE_NAME}"-latest.sql.zip"
  # Restore.
  wex db/restore -d=${LATEST_DUMP_FILE}
}
