#!/usr/bin/env bash

mailStart() {
  # Create temp dit if not exists.
  mkdir -p ${WEX_WEXAMPLE_DIR_MAIL_TMP}
  # Recompose
  wex wexample::mail/compose -c="up -d --build"
}