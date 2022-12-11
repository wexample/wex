#!/usr/bin/env bash

mastodonConfig() {

  echo "\nSITE_CONTAINER=mastodon"

  . .wex

  echo "\nMASTODON_VERSION=${MASTODON_VERSION}"
}
