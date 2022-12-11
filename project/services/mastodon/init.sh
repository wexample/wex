#!/usr/bin/env bash

mastodonInit() {
  # Override default container.
  echo "MASTODON_VERSION=v2.9.0" >> .wex

  . .wex

  # Generate key secret
  # docker-compose -f tmp/docker-compose.build.yml run --rm ${SITE_NAME}_mastodon rake secret
  # Generate vapid ket
  # docker-compose -f tmp/docker-compose.build.yml run --rm ${SITE_NAME}_mastodon rake mastodon:webpush:generate_vapid_key
  # docker-compose -f tmp/docker-compose.build.yml run --rm ${SITE_NAME}_mastodon chown -R 991:991 /mastodon/public/
  # Init script.
  docker-compose -f tmp/docker-compose.build.yml run --rm ${SITE_NAME}_mastodon bundle exec rake mastodon:setup
}
