#!/usr/bin/env bash

envCredentialsClear() {
  unset SITE_NAME
  unset SITE_USERNAME
  unset SITE_PRIVATE_KEY
  unset SITE_IPV4
  unset SITE_PORT
  # We may set it somewhere else.
  unset SITE_PATH_ROOT
}
