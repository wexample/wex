#!/usr/bin/env bash

wordpress5Init() {
  # Wordpress version
    cat <<EOF >> .wex

# Wordpress 5
WP_DB_CHARSET=utf8                          # Database charset
WP_DB_TABLE_PREFIX=wp_                      # Used for wordpress database
WP_DEBUG_ENABLED=false                      # Will allow wordpress debug mode
WP_VERSION=5.6.1-fpm-alpine                 # Docker image tags
EOF
}
