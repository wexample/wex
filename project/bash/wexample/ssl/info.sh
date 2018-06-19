#!/usr/bin/env bash

sslInfo() {
  docker exec wex_reverse_proxy_certs /app/cert_status
}