#!/usr/bin/env bash

n8nConfig() {
  . .wex
  # Override default container.
  echo "\nSITE_CONTAINER=n8n"
  echo "\nN8N_VERSION="${N8N_VERSION}
  echo "\nN8N_BASIC_AUTH_USER="${N8N_BASIC_AUTH_USER}
  echo "\nN8N_GENERIC_TIMEZONE="${N8N_GENERIC_TIMEZONE}
}
